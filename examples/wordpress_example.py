"""
Example usage of the WordPress REST API client.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from wordpress import WordPressClient
from common.config import ConfigManager

# Load configuration from .env file or environment variables
config = ConfigManager()
config.load_from_env()

# You can also load from a JSON file
# config.load_from_file("config.json")

def main():
    """Run the WordPress API example."""
    
    # Get WordPress credentials from config or set them directly
    wp_url = config.get("wordpress.url", "https://example.com/wp-json")
    wp_username = config.get("wordpress.username")
    wp_password = config.get("wordpress.password")
    
    # Initialize the WordPress client
    wp_client = WordPressClient(
        base_url=wp_url,
        username=wp_username,
        password=wp_password
    )
    
    print(f"Connected to WordPress site: {wp_url}")
    
    # Example 1: Get recent posts
    print("\n=== Recent Posts ===")
    try:
        posts = wp_client.get_posts(limit=5)
        for post in posts:
            print(f"- {post['title']['rendered']} (ID: {post['id']})")
    except Exception as e:
        print(f"Error getting posts: {e}")
    
    # Example 2: Get categories
    print("\n=== Categories ===")
    try:
        categories = wp_client.get_categories(limit=10)
        for category in categories:
            print(f"- {category['name']} (ID: {category['id']})")
    except Exception as e:
        print(f"Error getting categories: {e}")
    
    # Example 3: Create a new post (if credentials are provided)
    if wp_username and wp_password:
        print("\n=== Creating a New Post ===")
        try:
            new_post = wp_client.create_post(
                title="Test Post from Boompah Connect",
                content="This is a test post created using the Boompah Connect WordPress API client.",
                status="draft"
            )
            print(f"Created new post: {new_post['title']['rendered']} (ID: {new_post['id']})")
        except Exception as e:
            print(f"Error creating post: {e}")
    
    print("\nExample completed.")


if __name__ == "__main__":
    main()
