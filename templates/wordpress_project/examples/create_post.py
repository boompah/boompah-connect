"""
Example script to create a new post in WordPress.
"""

import sys
import os
import json
from pprint import pprint

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wp_client import wp_client

def main():
    """Create a new WordPress post."""
    try:
        # Create a new post (default status is "draft")
        title = "New Post from WordPress API"
        content = """
        <h2>Hello from WordPress API!</h2>
        <p>This post was created programmatically using the WordPress REST API.</p>
        <p>The integration is working correctly.</p>
        """
        
        # Optional parameters
        excerpt = "A post created via the WordPress REST API"
        
        # Create the post
        new_post = wp_client.create_post(
            title=title,
            content=content,
            excerpt=excerpt,
            status="draft"  # Use "publish" to publish immediately
        )
        
        print(f"Created new post:")
        print(f"Title: {new_post['title']['rendered']}")
        print(f"ID: {new_post['id']}")
        print(f"Status: {new_post['status']}")
        print(f"Link: {new_post['link']}")
        
        # Optionally save to JSON file
        with open('new_post.json', 'w') as f:
            json.dump(new_post, f, indent=2)
            print(f"\nSaved post details to new_post.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
