# Boompah Connect

A modular template project for storing connections to various APIs. This project provides standardized interfaces for connecting to different services, starting with WordPress REST API.

## Features

- Separate modules for each API connection
- Common utilities for API client implementation
- Configuration management for API credentials
- Standardized error handling
- Comprehensive documentation for both human and AI users

## Supported APIs

- WordPress REST API

## Project Structure

```
boompah-connect/
├── common/            # Common utilities shared across API connections
│   ├── api_client.py  # Base API client class
│   └── config.py      # Configuration management
├── wordpress/         # WordPress REST API connection
│   ├── __init__.py
│   └── client.py      # WordPress client implementation
├── examples/          # Example usage scripts
└── ...                # Additional API connections will be added here
```

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from wordpress import WordPressClient

# Initialize the WordPress API client
wp_client = WordPressClient(
    base_url="https://example.com/wp-json",
    username="your_username",
    password="your_password"
)

# Get posts
posts = wp_client.get_posts(limit=5)
print(posts)
```

## For AI Assistants

This library is designed with AI usage in mind. Each API module follows a consistent pattern:

1. Import the specific API client from its module
2. Initialize a client with required credentials
3. Use the client methods to interact with the API

The library handles authentication, request formatting, and error handling internally.

## Contributing

To add support for a new API:

1. Create a new directory for the API (e.g., `shopify/`)
2. Implement a client class that extends the base `APIClient`
3. Add appropriate documentation and examples

## License

MIT
