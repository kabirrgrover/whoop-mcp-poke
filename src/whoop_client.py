"""
WHOOP API client for authentication and data retrieval.
"""
import asyncio
import logging
import time
from typing import Optional, Dict, Any
import httpx

logger = logging.getLogger(__name__)


class WhoopClient:
    """Client for interacting with the WHOOP API."""
    
    BASE_URL = "https://api.prod.whoop.com"
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize the WHOOP client.
        
        Args:
            email: WHOOP account email
            password: WHOOP account password
        """
        self.email = email
        self.password = password
        self.access_token: Optional[str] = None
        self.token_expires_at: Optional[float] = None
        self.user_id: Optional[int] = None
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _authenticate(self) -> None:
        """Authenticate with WHOOP API using AWS Cognito."""
        if not self.email or not self.password:
            raise ValueError("WHOOP_EMAIL and WHOOP_PASSWORD must be set")
        
        url = f"{self.BASE_URL}/auth-service/v3/whoop"
        
        headers = {
            "Host": "api.prod.whoop.com",
            "Accept": "*/*",
            "Content-Type": "application/x-amz-json-1.1",
            "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth",
        }
        
        payload = {
            "AuthParameters": {
                "USERNAME": self.email,
                "PASSWORD": self.password,
            },
            "ClientId": "",  # WHOOP uses empty client ID
            "AuthFlow": "USER_PASSWORD_AUTH",
        }
        
        try:
            response = await self.client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("AuthenticationResult"):
                raise ValueError("Login failed: No authentication result received")
            
            auth_result = data["AuthenticationResult"]
            self.access_token = auth_result.get("AccessToken")
            
            # Token expires in seconds (from AuthenticationResult.ExpiresIn)
            expires_in = auth_result.get("ExpiresIn", 86400)
            self.token_expires_at = time.time() + expires_in
            
            logger.info("Successfully authenticated with WHOOP API via AWS Cognito")
        except httpx.HTTPStatusError as e:
            logger.error(f"Authentication failed: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"Failed to authenticate with WHOOP API: {e.response.text}")
    
    async def _get_user_id(self) -> None:
        """Get the current user ID."""
        if not self.access_token:
            return
        
        url = f"{self.BASE_URL}/user/profile/basic"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            self.user_id = data.get("user_id")
        except Exception as e:
            logger.warning(f"Could not get user ID: {e}")
    
    async def _ensure_authenticated(self) -> None:
        """Ensure we have a valid access token."""
        if not self.access_token or (self.token_expires_at and time.time() >= self.token_expires_at - 300):
            # Re-authenticate if token expired or expiring soon (5 min buffer)
            await self._authenticate()
    
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make an authenticated request to the WHOOP API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
        """
        await self._ensure_authenticated()
        
        url = f"{self.BASE_URL}{endpoint}"
        
        # Headers matching reference implementation
        import datetime
        headers = {
            "Host": "api.prod.whoop.com",
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "*/*",
            "User-Agent": "iOS",
            "Content-Type": "application/json",
            "X-WHOOP-Device-Platform": "iOS",
            "X-WHOOP-Time-Zone": datetime.datetime.now().astimezone().tzname() or "UTC",
            "Locale": "en_US",
            "Currency": "USD",
        }
        
        try:
            response = await self.client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                # Token expired, try to re-authenticate once
                logger.warning("Token expired, re-authenticating...")
                await self._authenticate()
                headers["Authorization"] = f"Bearer {self.access_token}"
                response = await self.client.get(url, headers=headers, params=params)
                response.raise_for_status()
                return response.json()
            raise ValueError(f"API request failed: {e.response.status_code} - {e.response.text}")
    
    async def get_overview(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive overview data for a specific date.
        
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        from datetime import datetime
        date_param = date or datetime.now().strftime("%Y-%m-%d")
        params = {"date": date_param}
        
        # Using home service endpoint (matches reference implementation)
        home_data = await self._make_request("/home-service/v1/home", params)
        return home_data
    
    async def get_sleep(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detailed sleep analysis.
        
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        from datetime import datetime
        date_param = date or datetime.now().strftime("%Y-%m-%d")
        params = {"date": date_param}
        
        sleep_data = await self._make_request("/home-service/v1/deep-dive/sleep", params)
        return sleep_data
    
    async def get_recovery(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get recovery deep dive analysis.
        
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        from datetime import datetime
        date_param = date or datetime.now().strftime("%Y-%m-%d")
        params = {"date": date_param}
        
        recovery_data = await self._make_request("/home-service/v1/deep-dive/recovery", params)
        return recovery_data
    
    async def get_strain(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get strain deep dive analysis.
        
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        from datetime import datetime
        date_param = date or datetime.now().strftime("%Y-%m-%d")
        params = {"date": date_param}
        
        strain_data = await self._make_request("/home-service/v1/deep-dive/strain", params)
        return strain_data
    
    async def get_healthspan(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get healthspan analysis.
        
        Args:
            date: Date in YYYY-MM-DD format (defaults to today)
        """
        from datetime import datetime
        date_param = date or datetime.now().strftime("%Y-%m-%d")
        params = {"date": date_param}
        
        healthspan_data = await self._make_request("/healthspan-service/v1/healthspan/bff", params)
        return healthspan_data
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

