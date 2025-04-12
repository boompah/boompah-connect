"""
Configuration management for WordPress REST API projects.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project information for custom user agent
PROJECT_NAME = "WordPress-Project"
PROJECT_VERSION = "1.0.0"

# WordPress API configuration
WP_BASE_URL = os.getenv("WP_BASE_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_AUTH_TOKEN = os.getenv("WP_AUTH_TOKEN")

# Validate required configuration
if not WP_BASE_URL:
    raise ValueError("WP_BASE_URL environment variable is required")

if not (WP_USERNAME and WP_PASSWORD) and not WP_AUTH_TOKEN:
    raise ValueError("Either WP_USERNAME and WP_PASSWORD or WP_AUTH_TOKEN environment variables are required")
