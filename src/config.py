"""
Configuration management for the MCP server.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    port: int = 3000
    mcp_auth_token: Optional[str] = None
    
    # WHOOP API credentials
    whoop_email: Optional[str] = None
    whoop_password: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()

