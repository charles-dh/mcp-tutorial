from typing import Any, Dict, List, Optional
import httpx

from mcp.server.fastmcp import FastMCP

# Initialize MCP
mcp = FastMCP("jokes")


# constants
URL = "https://official-joke-api.appspot.com/"


async def make_a_joke_request(endpoint: str) -> Optional[Dict[str, Any]]:
    """Make a request to the jokes API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL + endpoint, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_joke(joke: dict[str, Any] | None) -> str:
    """Format a joke dict into readable joke."""
    if joke:
        return f"""{joke.get("setup")}
---
{joke.get("punchline")}
"""
    else:
        return ""


@mcp.tool()
async def get_random_joke() -> str:
    """Get a random joke from the jokes API.
    """
    endpoint = "jokes/random"

    data = await make_a_joke_request(endpoint)

    if not data:
        return "Unable to fetch joke."
    return format_joke(data)
    

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')