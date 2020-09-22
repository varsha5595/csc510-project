#!/usr/bin/ev python3
from pathlib import Path
import setuptools

project_dir = Path(__file__).parent

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sync-ends",
    version="1.0.0",
    author="Adithya Ganesh, Meghana Vasist, Shivaprakash, Surbhi Jha, Varsha Sharma",
    author_email="varsha95.ananth@gmail.com",
    description="Extension to Slack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["python"],
    url="https://github.com/varsha5595/csc510-project",
    packages=setuptools.find_packages(),
    packages_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)