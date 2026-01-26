"""Sphinx configuration."""

from datetime import datetime

project = "Météo-France API"
author = "HACF (created by @oncleben31 & @Quentame, maintained by @Quentame)"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
