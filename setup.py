#!/usr/bin/ev python3
from pathlib import Path
import setuptools

project_dir = Path(__file__).parent


def get_requirements(filename):
    with open(filename, encoding="utf-8") as f:
        requirements = f.read().splitlines()
    return requirements


def get_long_description(filename):
    with open(filename, "r", encoding="utf-8") as fh:
        long_description = fh.read()
    return long_description


setuptools.setup(
    name="sync-ends",
    version="v2.1.3",
    author="Chintan Gandhi, Jay Modi, Suraj Patel, Omkar Kulkarni, Nirav Shah, Matthew Sills, Varun Deepak Gudhe, Sasank Marabattula",
    author_email="cagandhi97@gmail.com",
    description="Sync Ends - End Development Overheads CSC 510 Project",
    long_description=get_long_description("README.md"),
    long_description_content_type="text/markdown",
    keywords=["python"],
    url="https://github.com/smarabattula/Sync-Ends",
    download_url='https://github.com/jaymodi98/Sync-Ends/archive/v2.1.3.tar.gz',  # noqa: E501
    entry_points="""
    [console_scripts]
    syncends = src.main:main
    """,
    packages=setuptools.find_packages(),
    packages_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=get_requirements("requirements.txt"),
    include_package_data=True,
    python_requires=">=3.6",
)
