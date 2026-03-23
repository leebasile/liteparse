"""pypdf-compatible PdfReader powered by LiteParse."""

from __future__ import annotations

import io
import tempfile
from pathlib import Path
from typing import IO, Any, Dict, List, Optional, Union

from liteparse import LiteParse, ParseResult, ParsedPage
from ._page import PageObject
from ._meta import DocumentInformation


class PdfReader:
    """
    Drop-in replacement for pypdf.PdfReader backed by LiteParse.

    Supports the most commonly used pypdf.PdfReader interface so existing code
    can switch parsers by changing only the import line::

        # Before
        from pypdf import PdfReader

        # After
        from liteparse_pypdf import PdfReader

    Args:
        stream: A file path (str/Path), file-like object, or bytes.
        password: Password for encrypted PDFs.
        strict: Accepted for compatibility; ignored.
    """

    def __init__(
        self,
        stream: Union[str, Path, IO[bytes], bytes],
        password: Optional[str] = None,
        strict: bool = False,
        *,
        # LiteParse-specific options
        ocr_enabled: bool = True,
        ocr_server_url: Optional[str] = None,
        ocr_language: str = "en",
        dpi: int = 150,
        precise_bounding_box: bool = True,
    ) -> None:
        self._parser = LiteParse()
        self._password = password
        self._ocr_enabled = ocr_enabled
        self._ocr_server_url = ocr_server_url
        self._ocr_language = ocr_language
        self._dpi = dpi
        self._precise_bounding_box = precise_bounding_box

        # Resolve the input to a file path that liteparse can consume
        self._tmp_file: Optional[tempfile.NamedTemporaryFile] = None  # type: ignore[type-arg]
        file_path = self._resolve_input(stream)

        # Parse immediately (same as pypdf which reads on construction)
        self._result: ParseResult = self._parser.parse(
            file_path,
            ocr_enabled=self._ocr_enabled,
            ocr_server_url=self._ocr_server_url,
            ocr_language=self._ocr_language,
            dpi=self._dpi,
            precise_bounding_box=self._precise_bounding_box,
        )

        # Build page objects
        self._pages: List[PageObject] = [
            PageObject(page) for page in self._result.pages
        ]

    # ------------------------------------------------------------------
    # pypdf-compatible public API
    # ------------------------------------------------------------------

    @property
    def pages(self) -> List[PageObject]:
        """List of :class:`PageObject` instances (0-indexed)."""
        return self._pages

    @property
    def metadata(self) -> Optional[DocumentInformation]:
        """Document metadata (limited — LiteParse does not extract all PDF metadata)."""
        return DocumentInformation()

    @property
    def is_encrypted(self) -> bool:
        """Whether the document required a password."""
        return self._password is not None

    @property
    def pdf_header(self) -> str:
        """PDF header string. Not available from LiteParse; returns a default."""
        return "%PDF-1.7"

    def get_num_pages(self) -> int:  # noqa: D401 – legacy API name
        """Return number of pages (legacy helper, prefer ``len(reader.pages)``)."""
        return len(self._pages)

    @property
    def numPages(self) -> int:  # noqa: N802 – matches PyPDF2 legacy name
        """Number of pages (PyPDF2 compatibility alias)."""
        return len(self._pages)

    def getPage(self, page_number: int) -> PageObject:  # noqa: N802
        """Get page by index (PyPDF2 compatibility alias)."""
        return self._pages[page_number]

    def get_page(self, page_number: int) -> PageObject:
        """Get page by 0-based index."""
        return self._pages[page_number]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _resolve_input(self, stream: Union[str, Path, IO[bytes], bytes]) -> Path:
        """Convert various input types to a file path."""
        if isinstance(stream, (str, Path)):
            return Path(stream)

        # bytes or file-like → write to temp file
        if isinstance(stream, bytes):
            data = stream
        elif isinstance(stream, io.IOBase) or hasattr(stream, "read"):
            data = stream.read()  # type: ignore[union-attr]
        else:
            raise TypeError(f"Unsupported stream type: {type(stream)}")

        tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        tmp.write(data)
        tmp.flush()
        self._tmp_file = tmp
        return Path(tmp.name)

    def close(self) -> None:
        """Clean up temporary files."""
        if self._tmp_file is not None:
            try:
                Path(self._tmp_file.name).unlink(missing_ok=True)
            except OSError:
                pass
            self._tmp_file = None

    def __del__(self) -> None:
        self.close()

    def __enter__(self) -> "PdfReader":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def __len__(self) -> int:
        return len(self._pages)

    def __repr__(self) -> str:
        return f"PdfReader(pages={len(self._pages)})"
