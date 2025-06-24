from typing import Any, Dict, List
import httpx

from mcp.server.fastmcp import FastMCP

# Initialize MCP
mcp = FastMCP("quotes")


# constants
uri = "https://api.quotable.io/"

async def make_a_quote_request(uri: str, params: dict) -> list[dict[str, Any]] | None:
    """Make a request to the quotes API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(uri, timeout=30, params=params)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_quote(quote: dict[str, Any] | None) -> str:
    """Format a quote dict into readable quote."""
    if quote:
        return f"""{quote.get("content")}
---
{quote.get("author")}
"""
    else:
        return ""


@mcp.tool()
async def get_quotes(n: int = 1) -> str:
    """Get n quotes from the quotes API.
    
    Args:
        n: number of quotes to get. Default: 1, maximum 50.
    """
    uri = "quotes/random"
    params = {"limit": n}

    data = await make_a_quote_request(uri, params)

    if not data:
        return "Unable to fetch quote."
    quotes = [format_quote(quote) for quote in data]
    return " ".join(quotes)
    

if "__name__" == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')