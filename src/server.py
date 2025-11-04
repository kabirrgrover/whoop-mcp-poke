"""
WHOOP MCP Server - Poke Compatible
Based on InteractionCo/mcp-server-template
"""
import os
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("WHOOP MCP Server")

# WHOOP credentials from environment
WHOOP_EMAIL = os.getenv("WHOOP_EMAIL")
WHOOP_PASSWORD = os.getenv("WHOOP_PASSWORD")

# Import WHOOP modules (delayed to avoid circular imports)
import sys
sys.path.insert(0, os.path.dirname(__file__))

from whoop_client import WhoopClient
from tools.whoop import (
    handle_overview,
    handle_sleep,
    handle_recovery,
    handle_strain,
    handle_healthspan
)

# Global WHOOP client
_whoop_client = None

def get_whoop_client():
    """Get or create WHOOP client instance."""
    global _whoop_client
    if _whoop_client is None:
        _whoop_client = WhoopClient(email=WHOOP_EMAIL, password=WHOOP_PASSWORD)
    return _whoop_client


@mcp.tool()
def test_connection() -> str:
    """Test tool to verify MCP server is working."""
    return "✅ MCP Server is working! Connection successful."


@mcp.tool()
async def whoop_get_overview(date: str = None) -> str:
    """Get comprehensive Whoop overview data for a specific date."""
    client = get_whoop_client()
    result = await handle_overview(client, date)
    if result.get("content"):
        return result["content"][0]["text"]
    return "No data available"


@mcp.tool()
async def whoop_get_sleep(date: str = None) -> str:
    """Get detailed sleep analysis and performance metrics."""
    client = get_whoop_client()
    result = await handle_sleep(client, date)
    if result.get("content"):
        return result["content"][0]["text"]
    return "No data available"


@mcp.tool()
async def whoop_get_recovery(date: str = None) -> str:
    """Get recovery analysis with HRV, RHR, and trends."""
    client = get_whoop_client()
    result = await handle_recovery(client, date)
    if result.get("content"):
        return result["content"][0]["text"]
    return "No data available"


@mcp.tool()
async def whoop_get_strain(date: str = None) -> str:
    """Get strain analysis with heart rate zones and activities."""
    client = get_whoop_client()
    result = await handle_strain(client, date)
    if result.get("content"):
        return result["content"][0]["text"]
    return "No data available"


@mcp.tool()
async def whoop_get_healthspan(date: str = None) -> str:
    """Get biological age and pace of aging metrics."""
    client = get_whoop_client()
    result = await handle_healthspan(client, date)
    if result.get("content"):
        return result["content"][0]["text"]
    return "No data available"


# Run the server - matching Poke template exactly
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"🚀 Starting WHOOP MCP Server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
