"""
WordPress REST API client implementation.
"""

import base64
from typing import Dict, Any, Optional, List, Union
import logging

from common.api_client import APIClient

logger = logging.getLogger(__name__)


class WordPressClient(APIClient):
    """Client for the WordPress REST API."""
    
    def __init__(
        self,
        base_url: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        auth_token: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Initialize the WordPress API client.
        
        Args:
            base_url: The base URL for the WordPress site (e.g., https://example.com/wp-json)
            username: WordPress username for authentication
            password: WordPress password for authentication
            auth_token: JWT authentication token (if using JWT authentication)
            user_agent: Custom user agent string (recommended for security when using application passwords)
        """
        # Initialize with custom user agent if provided
        self.user_agent = user_agent
        super().__init__(base_url)
        
        # Set up authentication
        self.username = username
        self.password = password
        self.auth_token = auth_token
        
        # Configure authentication headers if credentials are provided
        if username and password:
            auth_string = f"{username}:{password}"
            encoded_auth = base64.b64encode(auth_string.encode()).decode()
            self.session.headers.update({"Authorization": f"Basic {encoded_auth}"})
        elif auth_token:
            self.session.headers.update({"Authorization": f"Bearer {auth_token}"})
    
    def _get_default_headers(self) -> Dict[str, str]:
        """
        Get default headers for WordPress API requests.
        
        Returns:
            Dictionary of default headers
        """
        headers = super()._get_default_headers()
        headers["Content-Type"] = "application/json"
        
        # Set custom user agent if provided (for security best practices with application passwords)
        if self.user_agent:
            headers["User-Agent"] = self.user_agent
            
        return headers
    
    # Posts
    def get_posts(
        self,
        limit: int = 10,
        page: int = 1,
        search: Optional[str] = None,
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        status: str = "publish"
    ) -> List[Dict[str, Any]]:
        """
        Get WordPress posts.
        
        Args:
            limit: Number of posts to retrieve (per_page parameter)
            page: Page number
            search: Search term
            categories: List of category IDs
            tags: List of tag IDs
            status: Post status (publish, draft, etc.)
            
        Returns:
            List of posts
        """
        params = {
            "per_page": limit,
            "page": page,
            "status": status
        }
        
        if search:
            params["search"] = search
            
        if categories:
            params["categories"] = ",".join(map(str, categories))
            
        if tags:
            params["tags"] = ",".join(map(str, tags))
            
        return self.get("wp/v2/posts", params=params)
    
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """
        Get a specific WordPress post by ID.
        
        Args:
            post_id: Post ID
            
        Returns:
            Post data
        """
        return self.get(f"wp/v2/posts/{post_id}")
    
    def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        excerpt: Optional[str] = None,
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        featured_media: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a new WordPress post.
        
        Args:
            title: Post title
            content: Post content
            status: Post status (draft, publish, etc.)
            excerpt: Post excerpt
            categories: List of category IDs
            tags: List of tag IDs
            featured_media: Featured image ID
            
        Returns:
            Created post data
        """
        data = {
            "title": title,
            "content": content,
            "status": status
        }
        
        if excerpt:
            data["excerpt"] = excerpt
            
        if categories:
            data["categories"] = categories
            
        if tags:
            data["tags"] = tags
            
        if featured_media:
            data["featured_media"] = featured_media
            
        return self.post("wp/v2/posts", json=data)
    
    def update_post(
        self,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[str] = None,
        excerpt: Optional[str] = None,
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        featured_media: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Update an existing WordPress post.
        
        Args:
            post_id: Post ID
            title: Post title
            content: Post content
            status: Post status (draft, publish, etc.)
            excerpt: Post excerpt
            categories: List of category IDs
            tags: List of tag IDs
            featured_media: Featured image ID
            
        Returns:
            Updated post data
        """
        data = {}
        
        if title:
            data["title"] = title
            
        if content:
            data["content"] = content
            
        if status:
            data["status"] = status
            
        if excerpt:
            data["excerpt"] = excerpt
            
        if categories:
            data["categories"] = categories
            
        if tags:
            data["tags"] = tags
            
        if featured_media:
            data["featured_media"] = featured_media
            
        return self.post(f"wp/v2/posts/{post_id}", json=data)
    
    def delete_post(self, post_id: int, force: bool = False) -> Dict[str, Any]:
        """
        Delete a WordPress post.
        
        Args:
            post_id: Post ID
            force: Whether to force deletion (skip trash)
            
        Returns:
            Deletion response
        """
        params = {"force": "true" if force else "false"}
        return self.delete(f"wp/v2/posts/{post_id}", params=params)
    
    # Categories
    def get_categories(self, limit: int = 10, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get WordPress categories.
        
        Args:
            limit: Number of categories to retrieve
            page: Page number
            
        Returns:
            List of categories
        """
        params = {
            "per_page": limit,
            "page": page
        }
        return self.get("wp/v2/categories", params=params)
    
    # Tags
    def get_tags(self, limit: int = 10, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get WordPress tags.
        
        Args:
            limit: Number of tags to retrieve
            page: Page number
            
        Returns:
            List of tags
        """
        params = {
            "per_page": limit,
            "page": page
        }
        return self.get("wp/v2/tags", params=params)
    
    # Media
    def upload_media(
        self,
        file_path: str,
        title: Optional[str] = None,
        caption: Optional[str] = None,
        alt_text: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Upload media to WordPress.
        
        Args:
            file_path: Path to the file to upload
            title: Media title
            caption: Media caption
            alt_text: Alternative text
            
        Returns:
            Uploaded media data
        """
        import os
        import mimetypes
        
        filename = os.path.basename(file_path)
        
        # Guess the MIME type based on the file extension
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-Type': mime_type,
        }
        
        with open(file_path, 'rb') as file:
            media_data = file.read()
        
        response = self.post("wp/v2/media", data=media_data, headers=headers)
        
        # Update media metadata if provided
        if title or caption or alt_text:
            media_id = response['id']
            metadata = {}
            
            if title:
                metadata['title'] = title
                
            if caption:
                metadata['caption'] = caption
                
            if alt_text:
                metadata['alt_text'] = alt_text
                
            if metadata:
                response = self.post(f"wp/v2/media/{media_id}", json=metadata)
                
        return response
    
    # Users
    def get_users(self, limit: int = 10, page: int = 1) -> List[Dict[str, Any]]:
        """
        Get WordPress users.
        
        Args:
            limit: Number of users to retrieve
            page: Page number
            
        Returns:
            List of users
        """
        params = {
            "per_page": limit,
            "page": page
        }
        return self.get("wp/v2/users", params=params)
    
    def get_me(self) -> Dict[str, Any]:
        """
        Get the current user's information.
        
        Returns:
            Current user data
        """
        return self.get("wp/v2/users/me")
    
    # Comments
    def get_comments(
        self,
        post_id: Optional[int] = None,
        limit: int = 10,
        page: int = 1
    ) -> List[Dict[str, Any]]:
        """
        Get WordPress comments.
        
        Args:
            post_id: Filter comments by post ID
            limit: Number of comments to retrieve
            page: Page number
            
        Returns:
            List of comments
        """
        params = {
            "per_page": limit,
            "page": page
        }
        
        if post_id:
            params["post"] = post_id
            
        return self.get("wp/v2/comments", params=params)
