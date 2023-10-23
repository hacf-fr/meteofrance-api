"""Sphinx configuration."""
from datetime import datetime


project = "meteofrance-api"
author = "HACF"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "furo",
]
autodoc_typehints = "description"
html_theme = "furo"
