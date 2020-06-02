"""Setup configuration."""
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    README = fh.read()
setup(
    name="meteofrance-api",
    version="0.0.2",
    author="oncleben31",
    author_email="oncleben31@gmail.com",
    description="Python client for Météo-France API.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hacf-fr/meteofrance-api",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["requests", "pytz"],
    extras_require={
        "testing": ["pytest", "pytest-cov", "requests_mock", "flake8", "pydocstyle"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
