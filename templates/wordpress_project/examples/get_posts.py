"""
Example script to fetch posts from WordPress.
"""

import sys
import os
import json
from pprint import pprint

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wp_client import wp_client

def main():
    """Fetch and display WordPress posts."""
    try:
        # Get the latest 5 published posts
        posts = wp_client.get_posts(limit=5)
        
        print(f"Retrieved {len(posts)} posts:")
        for post in posts:
            print(f"\nTitle: {post['title']['rendered']}")
            print(f"ID: {post['id']}")
            print(f"Date: {post['date']}")
            print(f"Link: {post['link']}")
            print("-" * 50)
        
        # Optionally save to JSON file
        with open('posts.json', 'w') as f:
            json.dump(posts, f, indent=2)
            print(f"\nSaved posts to posts.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
