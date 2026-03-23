"""pypdf-compatible PageObject backed by a LiteParse ParsedPage."""

from __future__ import annotations

from decimal import Decimal
from typing import Any, Callable, Dict, List, Optional, Tuple

from liteparse.types import ParsedPage, TextItem


class PageObject:
    """
    Drop-in replacement for pypdf.PageObject.

    Wraps a :class:`liteparse.types.ParsedPage` and exposes the subset of the
    pypdf ``PageObject`` interface that is used by the vast majority of
    consuming code.
    """

    def __init__(self, parsed_page: ParsedPage) -> None:
        self._page = parsed_page

    # ------------------------------------------------------------------
    # pypdf-compatible properties
    # ------------------------------------------------------------------

    @property
    def page_number(self) -> int:
        """0-based page index (pypdf convention)."""
        return self._page.pageNum - 1  # liteparse is 1-indexed

    @property
    def mediabox(self) -> _RectangleObject:
        """Page media box as a rectangle ``[0, 0, width, height]``."""
        return _RectangleObject(0, 0, self._page.width, self._page.height)

    @property
    def cropbox(self) -> _RectangleObject:
        """Crop box (defaults to mediabox)."""
        return self.mediabox

    @property
    def trimbox(self) -> _RectangleObject:
        """Trim box (defaults to mediabox)."""
        return self.mediabox

    @property
    def width(self) -> Decimal:
        """Page width in PDF points."""
        return Decimal(str(self._page.width))

    @property
    def height(self) -> Decimal:
        """Page height in PDF points."""
        return Decimal(str(self._page.height))

    @property
    def rotation(self) -> int:
        """Page rotation in degrees (not available from LiteParse, defaults to 0)."""
        return 0

    # ------------------------------------------------------------------
    # Text extraction
    # ------------------------------------------------------------------

    def extract_text(
        self,
        *args: Any,
        extraction_mode: str = "plain",
        visitor_text: Optional[Callable[..., None]] = None,
        **kwargs: Any,
    ) -> str:
        """
        Extract text from the page.

        This always uses LiteParse's spatial text extraction regardless of
        ``extraction_mode``.  The ``visitor_text`` callback is supported with
        the signature ``(text, None, None, None, None) -> None`` — the
        transformation matrices are not available from LiteParse.

        Args:
            extraction_mode: Accepted for compatibility; both "plain" and
                "layout" map to LiteParse's spatial extraction.
            visitor_text: Optional callback invoked per text item.

        Returns:
            The page text as a string.
        """
        if visitor_text is not None:
            for item in self._page.textItems:
                visitor_text(item.str, None, None, None, None)

        return self._page.text

    def extractText(self, *args: Any, **kwargs: Any) -> str:  # noqa: N802
        """Legacy PyPDF2 method name."""
        return self.extract_text(*args, **kwargs)

    # ------------------------------------------------------------------
    # LiteParse extras (not in pypdf, but useful)
    # ------------------------------------------------------------------

    @property
    def text_items(self) -> List[TextItem]:
        """Access the underlying LiteParse text items with coordinates."""
        return self._page.textItems

    @property
    def bounding_boxes(self) -> list:  # type: ignore[type-arg]
        """Access the underlying LiteParse bounding boxes."""
        return self._page.boundingBoxes

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"PageObject(page_number={self.page_number})"


class _RectangleObject:
    """Minimal rectangle matching pypdf's RectangleObject interface."""

    def __init__(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self._coords = (
            Decimal(str(x1)),
            Decimal(str(y1)),
            Decimal(str(x2)),
            Decimal(str(y2)),
        )

    @property
    def left(self) -> Decimal:
        return self._coords[0]

    @property
    def bottom(self) -> Decimal:
        return self._coords[1]

    @property
    def right(self) -> Decimal:
        return self._coords[2]

    @property
    def top(self) -> Decimal:
        return self._coords[3]

    @property
    def width(self) -> Decimal:
        return self._coords[2] - self._coords[0]

    @property
    def height(self) -> Decimal:
        return self._coords[3] - self._coords[1]

    def __getitem__(self, index: int) -> Decimal:
        return self._coords[index]

    def __len__(self) -> int:
        return 4

    def __repr__(self) -> str:
        return f"RectangleObject([{self.left}, {self.bottom}, {self.right}, {self.top}])"
