"""
Base API client implementation that serves as a foundation for all API clients.
"""

import requests
from typing import Dict, Any, Optional, Union, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    """Base class for all API clients."""
    
    def __init__(self, base_url: str):
        """
        Initialize the API client.
        
        Args:
            base_url: The base URL for the API.
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a request to the API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint to call
            params: Query parameters
            data: Form data
            json: JSON data
            headers: Request headers
            
        Returns:
            Response data as dictionary or list
            
        Raises:
            requests.HTTPError: If the request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        default_headers = self._get_default_headers()
        if headers:
            default_headers.update(headers)
            
        logger.debug(f"Making {method} request to {url}")
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=default_headers
        )
        
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            # Try to get error details from response
            error_detail = ""
            try:
                error_detail = response.json()
            except:
                error_detail = response.text
                
            logger.error(f"Error details: {error_detail}")
            raise
        except ValueError:
            # Return empty dict if response is not JSON
            return {}
            
    def _get_default_headers(self) -> Dict[str, str]:
        """
        Get default headers for API requests.
        
        Returns:
            Dictionary of default headers
        """
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"BoomPahConnect/0.1.0"
        }
        
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a GET request."""
        return self._request("GET", endpoint, params=params, **kwargs)
        
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a POST request."""
        return self._request("POST", endpoint, data=data, json=json, **kwargs)
        
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, json: Optional[Dict[str, Any]] = None, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a PUT request."""
        return self._request("PUT", endpoint, data=data, json=json, **kwargs)
        
    def delete(self, endpoint: str, **kwargs) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        """Make a DELETE request."""
        return self._request("DELETE", endpoint, **kwargs)
