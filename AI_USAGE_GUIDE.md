# Boompah Connect: AI Usage Guide

This guide is specifically designed for AI assistants to effectively use the Boompah Connect project when helping users interact with various APIs.

## Overview

Boompah Connect is a modular template project for storing connections to various APIs. It provides standardized interfaces for connecting to different services with each API having its own dedicated folder. The project handles authentication, request formatting, and error handling internally, making it easier for both humans and AI assistants to work with external APIs.

## WordPress REST API

### Basic Usage Pattern

```python
from wordpress import WordPressClient

# Initialize the WordPress client
wp_client = WordPressClient(
    base_url="https://example.com/wp-json",  # WordPress site URL with /wp-json endpoint
    username="username",                     # Optional: WordPress username
    password="password"                      # Optional: WordPress password
)

# Now you can use the client to interact with the WordPress API
```

### Common Operations

#### Retrieving Posts

```python
# Get recent posts (defaults to 10 most recent published posts)
posts = wp_client.get_posts()

# Get a specific post by ID
post = wp_client.get_post(post_id=123)

# Search for posts
search_results = wp_client.get_posts(search="keyword", limit=5)

# Filter posts by category or tag IDs
category_posts = wp_client.get_posts(categories=[4, 7])
tag_posts = wp_client.get_posts(tags=[12, 45])
```

#### Creating Content

```python
# Create a new post (defaults to draft status)
new_post = wp_client.create_post(
    title="New Post Title",
    content="Post content with <strong>HTML</strong> formatting.",
    status="draft",  # Options: draft, publish, pending, private
    excerpt="Optional excerpt",
    categories=[4, 7],  # Optional category IDs
    tags=[12, 45]       # Optional tag IDs
)

# Update an existing post
updated_post = wp_client.update_post(
    post_id=123,
    title="Updated Title",
    content="Updated content"
)

# Delete a post
wp_client.delete_post(post_id=123, force=False)  # Set force=True to bypass trash
```

#### Working with Categories and Tags

```python
# Get categories
categories = wp_client.get_categories()

# Get tags
tags = wp_client.get_tags()
```

#### Working with Media

```python
# Upload media (requires file path)
media = wp_client.upload_media(
    file_path="/path/to/image.jpg",
    title="Image Title",
    caption="Image Caption",
    alt_text="Alternative Text"
)
```

### Error Handling

The library handles HTTP errors internally and provides meaningful error messages. When using the library, wrap API calls in try-except blocks to handle potential errors gracefully:

```python
try:
    posts = wp_client.get_posts()
    # Process posts
except Exception as e:
    # Handle error
    print(f"Error: {e}")
```

## Configuration Management

Boompah Connect provides a configuration manager to handle API credentials securely:

```python
from common.config import ConfigManager

# Create a config manager
config = ConfigManager()

# Load from environment variables (prefixed with BOOMPAH_)
config.load_from_env()

# Or load from a JSON file
config.load_from_file("config.json")

# Get configuration values
wp_url = config.get("wordpress.url", "https://example.com/wp-json")  # With default
wp_username = config.get("wordpress.username")  # No default
```

## Best Practices for AI Assistants

1. **Always check for credentials**: Before attempting to make authenticated requests, verify that the necessary credentials are available.

2. **Use appropriate error handling**: Wrap API calls in try-except blocks to handle potential errors gracefully.

3. **Respect WordPress content types**: When creating or updating content, be aware of the WordPress content types and their specific fields.

4. **Pagination awareness**: When retrieving lists of items, be aware that WordPress uses pagination. Use the `limit` and `page` parameters to navigate through results.

5. **Rate limiting**: Be mindful of making too many requests in a short period, as WordPress sites may have rate limiting in place.

6. **Security considerations**: Never hardcode credentials in scripts. Use environment variables or secure configuration files.

## Extending to Other APIs

When the library is extended to support additional APIs, this guide will be updated with specific usage instructions for each new API.
