import os

import anthropic
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Standardized system context (>1,024 tokens)
HEAVY_SYSTEM_PROMPT = """
                        You are an enterprise AI assistant with access to the full company API specs...
                    """ + (
    "\n- Rule: Always validate user parameters against JSON schema." * 100
)


class QueryRequest(BaseModel):
    user_query: str


@app.post("/v1/chat")
async def chat_endpoint(request: QueryRequest):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": HEAVY_SYSTEM_PROMPT,
                    "cache_control": {
                        "type": "ephemeral"  # enables 5-minute TTL caching
                    },
                }
            ],
            messages=[{"role": "user", "content": request.user_query}],
        )

        # Track cache performance metrics
        usage = response.usage
        return {
            "response": response.content[0].text,
            "usage": {
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "cache_creation_input_tokens": getattr(
                    usage, "cache_creation_input_tokens", 0
                ),
                "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0),
            },
        }
    except Exception as e:  # noqa
        raise HTTPException(status_code=500, detail=str(e))


# Entrypoint to run directly with `python main.py`
if __name__ == "__main__":
    uvicorn.run("test_caching:app", host="127.0.0.1", port=8000, reload=True)
