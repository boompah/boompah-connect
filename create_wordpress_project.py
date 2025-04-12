#!/usr/bin/env python3
"""
Create WordPress Project Script

This script creates a new WordPress REST API project from the template.
It copies the template files to a new directory and sets up the project.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def create_project(project_name, destination_path=None):
    """
    Create a new WordPress REST API project from the template.
    
    Args:
        project_name: Name of the project (will be used as directory name if destination_path not provided)
        destination_path: Optional path where to create the project
    """
    # Get the template directory
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'wordpress_project')
    
    if not os.path.exists(template_dir):
        print(f"Error: Template directory not found at {template_dir}")
        return False
    
    # Determine the destination directory
    if destination_path:
        project_dir = os.path.join(destination_path, project_name)
    else:
        project_dir = os.path.join(os.getcwd(), project_name)
    
    # Check if the destination directory already exists
    if os.path.exists(project_dir):
        overwrite = input(f"Directory {project_dir} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Project creation cancelled.")
            return False
        shutil.rmtree(project_dir)
    
    # Create the project directory
    os.makedirs(project_dir, exist_ok=True)
    
    # Copy template files to the project directory
    for item in os.listdir(template_dir):
        source = os.path.join(template_dir, item)
        destination = os.path.join(project_dir, item)
        
        if os.path.isdir(source):
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)
    
    print(f"WordPress REST API project '{project_name}' created successfully at {project_dir}")
    print("\nNext steps:")
    print(f"1. cd {project_name}")
    print("2. pip install -r requirements.txt")
    print("3. Copy .env.example to .env and update with your WordPress credentials")
    print("4. python main.py")
    
    return True

def main():
    """Main function to parse arguments and create the project."""
    parser = argparse.ArgumentParser(description='Create a new WordPress REST API project')
    parser.add_argument('project_name', help='Name of the project (will be used as directory name)')
    parser.add_argument('--path', '-p', help='Path where to create the project (default: current directory)')
    
    args = parser.parse_args()
    
    create_project(args.project_name, args.path)

if __name__ == "__main__":
    main()
