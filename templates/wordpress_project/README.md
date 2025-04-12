# WordPress REST API Project Template

This template provides a ready-to-use structure for creating Python applications that integrate with WordPress using the REST API via the boompah-connect library.

## Features

- Pre-configured WordPress API client
- Environment-based configuration
- Example scripts for common operations
- Interactive demo application
- Comprehensive documentation

## Project Structure

```
wordpress_project/
├── config.py             # Configuration management
├── wp_client.py          # WordPress API client wrapper
├── main.py               # Main application with interactive menu
├── examples/             # Example scripts
│   ├── get_posts.py      # Example of fetching posts
│   ├── create_post.py    # Example of creating a post
│   └── upload_media.py   # Example of uploading media
├── requirements.txt      # Python dependencies
└── .env.example          # Example environment variables
```

## Usage

### Creating a New Project

1. Copy this template to your project directory:
   ```bash
   cp -r /path/to/boompah-connect/templates/wordpress_project /path/to/your/new-project
   cd /path/to/your/new-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Edit `.env` with your WordPress site details:
     ```
     WP_BASE_URL=https://your-wordpress-site.com/wp-json
     WP_USERNAME=your_username
     WP_PASSWORD=your_password
     ```

### Running the Interactive Demo

```bash
python main.py
```

### Using the WordPress Client in Your Code

```python
from wp_client import wp_client

# Get recent posts
posts = wp_client.get_posts(limit=5)

# Create a new post
new_post = wp_client.create_post(
    title="Hello World",
    content="<p>This is my first post via the API!</p>",
    status="draft"
)
```

## Requirements

- Python 3.6+
- WordPress site with REST API enabled
- User credentials with appropriate permissions
