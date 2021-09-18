import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="learncloudops-utils",
    version="1.0.1",
    description="Useful OO abstractions for building aws cloud apps in Python",
    long_description_content_type="text/markdown",
    long_description=README,
    url="https://github.com/learncloudops/awsutils",
    author="learncloudops.com",
    email="matt@learncloudops.com",
    classifiers=["License :: OSI Approved :: MIT License",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.8"],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=['boto3']
)