from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="boompah-connect",
    version="0.1.0",
    author="Boompah",
    author_email="info@example.com",
    description="A modular template project for storing connections to various APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boompah/boompah-connect",
    packages=["common", "wordpress"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.1",
        "python-dotenv>=0.21.0",
    ],
)
