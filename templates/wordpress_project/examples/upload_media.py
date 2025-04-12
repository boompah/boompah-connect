"""
Example script to upload media to WordPress.
"""

import sys
import os
import json
from pprint import pprint

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wp_client import wp_client

def main():
    """Upload media to WordPress."""
    try:
        # Path to the image file to upload
        # Replace with an actual image path on your system
        image_path = "path/to/your/image.jpg"
        
        # Check if file exists
        if not os.path.exists(image_path):
            print(f"Error: File {image_path} does not exist.")
            print("Please update the script with a valid image path.")
            return
        
        # Upload the media file
        media = wp_client.upload_media(
            file_path=image_path,
            title="Image uploaded via WordPress API",
            caption="This image was uploaded via the WordPress REST API",
            alt_text="WordPress API image"
        )
        
        print(f"Uploaded media:")
        print(f"ID: {media['id']}")
        print(f"Title: {media['title']['rendered']}")
        print(f"URL: {media['source_url']}")
        
        # Optionally save to JSON file
        with open('media.json', 'w') as f:
            json.dump(media, f, indent=2)
            print(f"\nSaved media details to media.json")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
