"""
WHOOP tools for retrieving various fitness and health metrics.
"""
from typing import Any, Dict, Optional
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from whoop_client import WhoopClient


async def handle_overview(whoop_client: WhoopClient, date: Optional[str] = None) -> Dict[str, Any]:
    """
    Handle whoop_get_overview tool call.
    
    Retrieves comprehensive Whoop overview data for a specific date.
    """
    try:
        data = await whoop_client.get_overview(date)
        
        # Format the response based on WHOOP API structure
        # This structure may need adjustment based on actual API response
        formatted_text = format_overview_response(data)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted_text
                }
            ]
        }
    except Exception as e:
        error_msg = str(e) if isinstance(e, Exception) else "Unknown error"
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error fetching Whoop overview data: {error_msg}"
                }
            ],
            "isError": True
        }


async def handle_sleep(whoop_client: WhoopClient, date: Optional[str] = None) -> Dict[str, Any]:
    """Handle whoop_get_sleep tool call."""
    try:
        data = await whoop_client.get_sleep(date)
        formatted_text = format_sleep_response(data)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted_text
                }
            ]
        }
    except Exception as e:
        error_msg = str(e) if isinstance(e, Exception) else "Unknown error"
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error fetching Whoop sleep data: {error_msg}"
                }
            ],
            "isError": True
        }


async def handle_recovery(whoop_client: WhoopClient, date: Optional[str] = None) -> Dict[str, Any]:
    """Handle whoop_get_recovery tool call."""
    try:
        data = await whoop_client.get_recovery(date)
        formatted_text = format_recovery_response(data)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted_text
                }
            ]
        }
    except Exception as e:
        error_msg = str(e) if isinstance(e, Exception) else "Unknown error"
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error fetching Whoop recovery data: {error_msg}"
                }
            ],
            "isError": True
        }


async def handle_strain(whoop_client: WhoopClient, date: Optional[str] = None) -> Dict[str, Any]:
    """Handle whoop_get_strain tool call."""
    try:
        data = await whoop_client.get_strain(date)
        formatted_text = format_strain_response(data)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted_text
                }
            ]
        }
    except Exception as e:
        error_msg = str(e) if isinstance(e, Exception) else "Unknown error"
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error fetching Whoop strain data: {error_msg}"
                }
            ],
            "isError": True
        }


async def handle_healthspan(whoop_client: WhoopClient, date: Optional[str] = None) -> Dict[str, Any]:
    """Handle whoop_get_healthspan tool call."""
    try:
        data = await whoop_client.get_healthspan(date)
        formatted_text = format_healthspan_response(data)
        
        return {
            "content": [
                {
                    "type": "text",
                    "text": formatted_text
                }
            ]
        }
    except Exception as e:
        error_msg = str(e) if isinstance(e, Exception) else "Unknown error"
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error fetching Whoop healthspan data: {error_msg}"
                }
            ],
            "isError": True
        }


def format_overview_response(data: Dict[str, Any]) -> str:
    """Format overview data for display."""
    import json
    lines = [
        "📊 WHOOP OVERVIEW",
        "═══════════════════",
        ""
    ]
    
    # Display full data in formatted JSON
    try:
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        lines.append(formatted_data)
    except Exception as e:
        lines.append(f"✅ Overview data retrieved")
        lines.append(f"Raw data: {str(data)}")
    
    return "\n".join(lines)


def format_sleep_response(data: Dict[str, Any]) -> str:
    """Format sleep data for display."""
    import json
    lines = [
        "😴 SLEEP ANALYSIS",
        "═══════════════════",
        ""
    ]
    
    # Display full data in formatted JSON
    try:
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        lines.append(formatted_data)
    except Exception as e:
        lines.append(f"✅ Sleep data retrieved")
        lines.append(f"Raw data: {str(data)}")
    
    return "\n".join(lines)


def format_recovery_response(data: Dict[str, Any]) -> str:
    """Format recovery data for display."""
    import json
    lines = [
        "💚 RECOVERY ANALYSIS",
        "═══════════════════",
        ""
    ]
    
    # Display full data in formatted JSON
    try:
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        lines.append(formatted_data)
    except Exception as e:
        lines.append(f"✅ Recovery data retrieved")
        lines.append(f"Raw data: {str(data)}")
    
    return "\n".join(lines)


def format_strain_response(data: Dict[str, Any]) -> str:
    """Format strain data for display."""
    import json
    lines = [
        "🔥 STRAIN ANALYSIS",
        "═══════════════════",
        ""
    ]
    
    # Display full data in formatted JSON
    try:
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        lines.append(formatted_data)
    except Exception as e:
        lines.append(f"✅ Strain data retrieved")
        lines.append(f"Raw data: {str(data)}")
    
    return "\n".join(lines)


def format_healthspan_response(data: Dict[str, Any]) -> str:
    """Format healthspan data for display."""
    import json
    lines = [
        "⏳ HEALTHSPAN ANALYSIS",
        "═══════════════════",
        ""
    ]
    
    # Display full data in formatted JSON
    try:
        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        lines.append(formatted_data)
    except Exception as e:
        lines.append(f"✅ Healthspan data retrieved")
        lines.append(f"Raw data: {str(data)}")
    
    return "\n".join(lines)

