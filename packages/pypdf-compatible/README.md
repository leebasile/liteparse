# liteparse-pypdf-compatible

Drop-in replacement for [pypdf](https://github.com/py-pdf/pypdf) powered by [LiteParse](https://github.com/run-llama/liteparse) for higher quality text extraction.

## Installation

```bash
pip install liteparse-pypdf-compatible
```

**Prerequisite:** The LiteParse Node.js CLI must be installed:

```bash
npm install -g @llamaindex/liteparse
```

## Usage

Replace your pypdf import with liteparse_pypdf — no other code changes needed:

```python
# Before
from pypdf import PdfReader

# After
from liteparse_pypdf import PdfReader

reader = PdfReader("document.pdf")

for page in reader.pages:
    text = page.extract_text()
    print(text)

print(f"Number of pages: {len(reader.pages)}")
```

## Supported pypdf API

### PdfReader

| Property / Method | Status |
|---|---|
| `PdfReader(path_or_stream)` | Supported (str, Path, bytes, file-like) |
| `reader.pages` | Supported (list of PageObject) |
| `len(reader.pages)` | Supported |
| `reader.metadata` | Stub (returns None fields) |
| `reader.is_encrypted` | Supported |
| `reader.get_num_pages()` | Supported |
| `reader.get_page(n)` | Supported (0-indexed) |
| Context manager (`with`) | Supported |

### PageObject

| Property / Method | Status |
|---|---|
| `page.extract_text()` | Supported |
| `page.width` / `page.height` | Supported (Decimal) |
| `page.mediabox` | Supported |
| `page.cropbox` / `page.trimbox` | Supported (defaults to mediabox) |
| `page.rotation` | Stub (returns 0) |
| `page.page_number` | Supported (0-indexed) |
| `visitor_text` callback | Supported |

### LiteParse extras

Beyond the pypdf interface, pages expose additional LiteParse data:

```python
page = reader.pages[0]
page.text_items      # List of TextItem with x, y, width, height, font info
page.bounding_boxes  # List of BoundingBox with x1, y1, x2, y2
```

### LiteParse options

Pass LiteParse-specific options to the reader constructor:

```python
reader = PdfReader(
    "document.pdf",
    ocr_enabled=True,
    ocr_language="en",
    dpi=300,
)
```

## Unsupported

- `PdfWriter` — LiteParse is read-only
- PDF metadata extraction (title, author, etc.)
- Page-level transformations (`merge_page`, `add_transformation`)
- Form field operations
