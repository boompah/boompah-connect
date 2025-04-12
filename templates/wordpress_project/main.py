"""
WordPress REST API Integration - Main Application

This script demonstrates how to use the WordPress REST API integration
to interact with a WordPress site from your Python application.
"""

import os
import json
import logging
from pprint import pprint

from wp_client import wp_client
from config import WP_BASE_URL

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print(f"WordPress API Integration")
    print(f"Connected to: {WP_BASE_URL}")
    print("=" * 50)
    print("1. Get recent posts")
    print("2. Get post by ID")
    print("3. Create new post")
    print("4. Update existing post")
    print("5. Get categories")
    print("6. Get tags")
    print("7. Get user information")
    print("8. Exit")
    print("=" * 50)
    return input("Enter your choice (1-8): ")

def get_recent_posts():
    """Fetch and display recent posts."""
    try:
        limit = int(input("Number of posts to retrieve (default 5): ") or 5)
        posts = wp_client.get_posts(limit=limit)
        
        print(f"\nRetrieved {len(posts)} posts:")
        for post in posts:
            print(f"\nTitle: {post['title']['rendered']}")
            print(f"ID: {post['id']}")
            print(f"Date: {post['date']}")
            print(f"Link: {post['link']}")
            print("-" * 50)
            
        # Ask if user wants to save to file
        if input("\nSave posts to JSON file? (y/n): ").lower() == 'y':
            filename = input("Enter filename (default: posts.json): ") or "posts.json"
            with open(filename, 'w') as f:
                json.dump(posts, f, indent=2)
                print(f"Saved posts to {filename}")
    except Exception as e:
        logger.error(f"Error retrieving posts: {e}")
        print(f"Error: {e}")

def get_post_by_id():
    """Fetch and display a post by ID."""
    try:
        post_id = int(input("Enter post ID: "))
        post = wp_client.get_post(post_id)
        
        print(f"\nPost details:")
        print(f"Title: {post['title']['rendered']}")
        print(f"ID: {post['id']}")
        print(f"Date: {post['date']}")
        print(f"Status: {post['status']}")
        print(f"Link: {post['link']}")
        print(f"\nContent preview: {post['excerpt']['rendered'][:100]}...")
    except Exception as e:
        logger.error(f"Error retrieving post: {e}")
        print(f"Error: {e}")

def create_new_post():
    """Create a new WordPress post."""
    try:
        title = input("Enter post title: ")
        content = input("Enter post content (HTML supported): ")
        excerpt = input("Enter post excerpt (optional): ")
        
        status_options = {
            "1": "draft",
            "2": "publish",
            "3": "pending",
            "4": "private"
        }
        
        print("\nStatus options:")
        for key, value in status_options.items():
            print(f"{key}. {value}")
            
        status_choice = input("Select status (default: draft): ") or "1"
        status = status_options.get(status_choice, "draft")
        
        # Create the post
        post_data = {
            "title": title,
            "content": content,
            "status": status
        }
        
        if excerpt:
            post_data["excerpt"] = excerpt
            
        new_post = wp_client.create_post(**post_data)
        
        print(f"\nCreated new post:")
        print(f"Title: {new_post['title']['rendered']}")
        print(f"ID: {new_post['id']}")
        print(f"Status: {new_post['status']}")
        print(f"Link: {new_post['link']}")
    except Exception as e:
        logger.error(f"Error creating post: {e}")
        print(f"Error: {e}")

def update_existing_post():
    """Update an existing WordPress post."""
    try:
        post_id = int(input("Enter post ID to update: "))
        
        # First get the current post to show the user
        current_post = wp_client.get_post(post_id)
        print(f"\nCurrent post details:")
        print(f"Title: {current_post['title']['rendered']}")
        print(f"Status: {current_post['status']}")
        
        # Get update information
        title = input(f"Enter new title (leave empty to keep current): ")
        content = input(f"Enter new content (leave empty to keep current): ")
        
        status_options = {
            "1": "draft",
            "2": "publish",
            "3": "pending",
            "4": "private",
            "5": "Keep current"
        }
        
        print("\nStatus options:")
        for key, value in status_options.items():
            print(f"{key}. {value}")
            
        status_choice = input("Select status: ") or "5"
        status = status_options.get(status_choice, None)
        
        if status == "Keep current":
            status = None
            
        # Update the post
        update_data = {"post_id": post_id}
        
        if title:
            update_data["title"] = title
        if content:
            update_data["content"] = content
        if status:
            update_data["status"] = status
            
        updated_post = wp_client.update_post(**update_data)
        
        print(f"\nUpdated post:")
        print(f"Title: {updated_post['title']['rendered']}")
        print(f"ID: {updated_post['id']}")
        print(f"Status: {updated_post['status']}")
        print(f"Link: {updated_post['link']}")
    except Exception as e:
        logger.error(f"Error updating post: {e}")
        print(f"Error: {e}")

def get_categories():
    """Fetch and display WordPress categories."""
    try:
        categories = wp_client.get_categories(limit=20)
        
        print(f"\nRetrieved {len(categories)} categories:")
        for category in categories:
            print(f"ID: {category['id']} - Name: {category['name']} - Count: {category['count']}")
    except Exception as e:
        logger.error(f"Error retrieving categories: {e}")
        print(f"Error: {e}")

def get_tags():
    """Fetch and display WordPress tags."""
    try:
        tags = wp_client.get_tags(limit=20)
        
        print(f"\nRetrieved {len(tags)} tags:")
        for tag in tags:
            print(f"ID: {tag['id']} - Name: {tag['name']} - Count: {tag['count']}")
    except Exception as e:
        logger.error(f"Error retrieving tags: {e}")
        print(f"Error: {e}")

def get_user_info():
    """Fetch and display information about the current user."""
    try:
        user = wp_client.get_me()
        
        print(f"\nCurrent user information:")
        print(f"ID: {user['id']}")
        print(f"Name: {user['name']}")
        print(f"Username: {user['slug']}")
        print(f"Email: {user.get('email', 'Not available')}")
        print(f"Roles: {', '.join(user.get('roles', []))}")
    except Exception as e:
        logger.error(f"Error retrieving user information: {e}")
        print(f"Error: {e}")

def main():
    """Main application entry point."""
    print("Initializing WordPress integration...")
    
    try:
        # Test connection
        wp_client.get_me()
        logger.info("Successfully connected to WordPress API")
        
        while True:
            choice = display_menu()
            
            if choice == "1":
                get_recent_posts()
            elif choice == "2":
                get_post_by_id()
            elif choice == "3":
                create_new_post()
            elif choice == "4":
                update_existing_post()
            elif choice == "5":
                get_categories()
            elif choice == "6":
                get_tags()
            elif choice == "7":
                get_user_info()
            elif choice == "8":
                print("\nExiting WordPress integration. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")
                
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
