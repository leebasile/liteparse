"""liteparse-pypdf-compatible: drop-in pypdf replacement powered by LiteParse."""

from ._reader import PdfReader
from ._page import PageObject
from ._meta import DocumentInformation

__version__ = "0.1.0"
__all__ = [
    "PdfReader",
    "PageObject",
    "DocumentInformation",
]
