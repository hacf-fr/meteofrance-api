"""Fixtures used for testing the module."""


def get_file_content(filename: str) -> str:
    """Read fixture text file as string."""
    with open(filename, mode="r", encoding="utf-8") as file:
        content = file.read()
    return content
