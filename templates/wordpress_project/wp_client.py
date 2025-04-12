"""
WordPress API client for projects using boompah-connect.
This module provides a wrapper around the boompah-connect WordPress client.
"""

import sys
import os
import logging

# Add the boompah-connect directory to the Python path
# This assumes the boompah-connect package is installed or in the parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from wordpress.client import WordPressClient
except ImportError:
    raise ImportError("Could not import WordPressClient from boompah-connect. "
                     "Make sure the library is installed correctly.")

from config import WP_BASE_URL, WP_USERNAME, WP_PASSWORD, WP_AUTH_TOKEN, PROJECT_NAME, PROJECT_VERSION

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WordPressClientWrapper:
    """
    WordPress client wrapper.
    This class provides a simplified interface to the WordPress REST API
    using the boompah-connect library.
    """
    
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern for the WordPress client."""
        if cls._instance is None:
            cls._instance = super(WordPressClientWrapper, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the WordPress client with credentials from config."""
        logger.info(f"Initializing WordPress client with base URL: {WP_BASE_URL}")
        
        # Create custom user agent for security best practices when using application passwords
        custom_user_agent = f"{PROJECT_NAME}/{PROJECT_VERSION}"
        
        self.client = WordPressClient(
            base_url=WP_BASE_URL,
            username=WP_USERNAME,
            password=WP_PASSWORD,
            auth_token=WP_AUTH_TOKEN,
            user_agent=custom_user_agent
        )
        
        # Test connection
        try:
            self.client.get_me()
            logger.info("Successfully connected to WordPress API")
        except Exception as e:
            logger.error(f"Failed to connect to WordPress API: {e}")
            raise
    
    # Posts
    def get_posts(self, limit=10, page=1, **kwargs):
        """Get WordPress posts with optional filtering."""
        return self.client.get_posts(limit=limit, page=page, **kwargs)
    
    def get_post(self, post_id):
        """Get a specific WordPress post by ID."""
        return self.client.get_post(post_id)
    
    def create_post(self, title, content, **kwargs):
        """Create a new WordPress post."""
        return self.client.create_post(title=title, content=content, **kwargs)
    
    def update_post(self, post_id, **kwargs):
        """Update an existing WordPress post."""
        return self.client.update_post(post_id=post_id, **kwargs)
    
    def delete_post(self, post_id, force=False):
        """Delete a WordPress post."""
        return self.client.delete_post(post_id=post_id, force=force)
    
    # Categories
    def get_categories(self, limit=10, page=1):
        """Get WordPress categories."""
        return self.client.get_categories(limit=limit, page=page)
    
    # Tags
    def get_tags(self, limit=10, page=1):
        """Get WordPress tags."""
        return self.client.get_tags(limit=limit, page=page)
    
    # Media
    def upload_media(self, file_path, **kwargs):
        """Upload media to WordPress."""
        return self.client.upload_media(file_path=file_path, **kwargs)
    
    # Users
    def get_users(self, limit=10, page=1):
        """Get WordPress users."""
        return self.client.get_users(limit=limit, page=page)
    
    def get_me(self):
        """Get the current user's information."""
        return self.client.get_me()
    
    # Comments
    def get_comments(self, post_id=None, limit=10, page=1):
        """Get WordPress comments."""
        return self.client.get_comments(post_id=post_id, limit=limit, page=page)


# Create a singleton instance
wp_client = WordPressClientWrapper()
