import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sync-ends",
    version="0.0.1",
    author="Adithya Ganesh, Meghana Vasist, Shivaprakash, Surbhi Jha, Varsha Sharma",
    author_email="varsha95.ananth@gmail.com",
    description="Extension to Slack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/varsha5595/csc510-project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)