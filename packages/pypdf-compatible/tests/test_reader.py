"""Tests for the pypdf-compatible wrapper."""

from __future__ import annotations

from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from liteparse.types import BoundingBox, ParsedPage, ParseResult, TextItem

from liteparse_pypdf import PdfReader, PageObject, DocumentInformation
from liteparse_pypdf._page import _RectangleObject


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_parse_result(num_pages: int = 2) -> ParseResult:
    """Build a fake ParseResult for testing."""
    pages = []
    for i in range(1, num_pages + 1):
        pages.append(
            ParsedPage(
                pageNum=i,
                width=612.0,
                height=792.0,
                text=f"Page {i} text content",
                textItems=[
                    TextItem(
                        str=f"Hello from page {i}",
                        x=72.0, y=700.0,
                        width=100.0, height=12.0,
                        w=100.0, h=12.0, r=0,
                        fontName="Helvetica", fontSize=12.0,
                    ),
                ],
                boundingBoxes=[
                    BoundingBox(x1=72.0, y1=688.0, x2=172.0, y2=700.0),
                ],
            )
        )
    return ParseResult(
        pages=pages,
        text="\n\n".join(p.text for p in pages),
    )


# ---------------------------------------------------------------------------
# PdfReader tests
# ---------------------------------------------------------------------------

class TestPdfReader:
    """Tests for the PdfReader wrapper."""

    @patch("liteparse_pypdf._reader.LiteParse")
    def test_pages_length(self, MockLiteParse: MagicMock) -> None:
        mock_parser = MockLiteParse.return_value
        mock_parser.parse.return_value = _make_parse_result(3)

        reader = PdfReader("fake.pdf")

        assert len(reader.pages) == 3
        assert len(reader) == 3
        assert reader.get_num_pages() == 3
        assert reader.numPages == 3

    @patch("liteparse_pypdf._reader.LiteParse")
    def test_page_access(self, MockLiteParse: MagicMock) -> None:
        mock_parser = MockLiteParse.return_value
        mock_parser.parse.return_value = _make_parse_result(2)

        reader = PdfReader("fake.pdf")

        page = reader.pages[0]
        assert isinstance(page, PageObject)
        assert page.page_number == 0

        page1 = reader.get_page(1)
        assert page1.page_number == 1

        legacy = reader.getPage(0)
        assert legacy.page_number == 0

    @patch("liteparse_pypdf._reader.LiteParse")
    def test_metadata(self, MockLiteParse: MagicMock) -> None:
        mock_parser = MockLiteParse.return_value
        mock_parser.parse.return_value = _make_parse_result(1)

        reader = PdfReader("fake.pdf")
        meta = reader.metadata
        assert isinstance(meta, DocumentInformation)
        assert meta.title is None

    @patch("liteparse_pypdf._reader.LiteParse")
    def test_is_encrypted(self, MockLiteParse: MagicMock) -> None:
        mock_parser = MockLiteParse.return_value
        mock_parser.parse.return_value = _make_parse_result(1)

        reader = PdfReader("fake.pdf")
        assert reader.is_encrypted is False

        reader2 = PdfReader("fake.pdf", password="secret")
        assert reader2.is_encrypted is True

    @patch("liteparse_pypdf._reader.LiteParse")
    def test_context_manager(self, MockLiteParse: MagicMock) -> None:
        mock_parser = MockLiteParse.return_value
        mock_parser.parse.return_value = _make_parse_result(1)

        with PdfReader("fake.pdf") as reader:
            assert len(reader.pages) == 1

    @patch("liteparse_pypdf._reader.LiteParse")
    def test_bytes_input(self, MockLiteParse: MagicMock) -> None:
        mock_parser = MockLiteParse.return_value
        mock_parser.parse.return_value = _make_parse_result(1)

        reader = PdfReader(b"%PDF-1.7 fake content")
        assert len(reader.pages) == 1
        reader.close()


# ---------------------------------------------------------------------------
# PageObject tests
# ---------------------------------------------------------------------------

class TestPageObject:
    """Tests for the PageObject wrapper."""

    def _make_page(self) -> PageObject:
        parsed = ParsedPage(
            pageNum=1,
            width=612.0,
            height=792.0,
            text="Hello World",
            textItems=[
                TextItem(
                    str="Hello World", x=72.0, y=700.0,
                    width=100.0, height=12.0, w=100.0, h=12.0, r=0,
                ),
            ],
            boundingBoxes=[
                BoundingBox(x1=72.0, y1=688.0, x2=172.0, y2=700.0),
            ],
        )
        return PageObject(parsed)

    def test_extract_text(self) -> None:
        page = self._make_page()
        assert page.extract_text() == "Hello World"
        assert page.extractText() == "Hello World"

    def test_dimensions(self) -> None:
        page = self._make_page()
        assert page.width == Decimal("612.0")
        assert page.height == Decimal("792.0")

    def test_page_number(self) -> None:
        page = self._make_page()
        assert page.page_number == 0  # 0-indexed

    def test_mediabox(self) -> None:
        page = self._make_page()
        box = page.mediabox
        assert box.width == Decimal("612.0")
        assert box.height == Decimal("792.0")
        assert box[0] == Decimal("0")
        assert len(box) == 4

    def test_visitor_text(self) -> None:
        page = self._make_page()
        collected: list[str] = []

        def visitor(text: str, *args: object) -> None:
            collected.append(text)

        page.extract_text(visitor_text=visitor)
        assert collected == ["Hello World"]

    def test_text_items_extra(self) -> None:
        page = self._make_page()
        assert len(page.text_items) == 1
        assert page.text_items[0].str == "Hello World"

    def test_rotation_default(self) -> None:
        page = self._make_page()
        assert page.rotation == 0


# ---------------------------------------------------------------------------
# RectangleObject tests
# ---------------------------------------------------------------------------

class TestRectangleObject:
    def test_properties(self) -> None:
        rect = _RectangleObject(10, 20, 110, 120)
        assert rect.left == Decimal("10")
        assert rect.bottom == Decimal("20")
        assert rect.right == Decimal("110")
        assert rect.top == Decimal("120")
        assert rect.width == Decimal("100")
        assert rect.height == Decimal("100")

    def test_indexing(self) -> None:
        rect = _RectangleObject(0, 0, 100, 200)
        assert rect[2] == Decimal("100")
        assert rect[3] == Decimal("200")
