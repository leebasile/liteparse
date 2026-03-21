from pathlib import Path

import pymupdf4llm

from .base import ParserProvider


class PyMuPDF4LLMMarkdownProvider(ParserProvider):
    """
    Parse provider using PyMuPDF4LLM with markdown output.

    Install with: pip install pymupdf4llm
    """

    def __init__(self):
        """Initialize the parse provider."""
        pass

    def extract_text(self, file_path: Path) -> str:
        """Extract text from a document as markdown using PyMuPDF4LLM."""
        return pymupdf4llm.to_markdown(str(file_path))


class PyMuPDF4LLMTextProvider(ParserProvider):
    """
    Parse provider using PyMuPDF4LLM with plain text output.

    Install with: pip install pymupdf4llm
    """

    def __init__(self):
        """Initialize the parse provider."""
        pass

    def extract_text(self, file_path: Path) -> str:
        """Extract plain text from a document using PyMuPDF4LLM."""
        return pymupdf4llm.to_text(str(file_path))
