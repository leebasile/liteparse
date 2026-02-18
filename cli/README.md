# cli/

Command-line interface for LiteParse using Commander.js.

## Files

### parse.ts
**CLI entry point with two main commands: `parse` and `screenshot`.**

---

## Commands

### `liteparse parse <file>`
Parse documents and extract text.

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output <file>` | Save output to file | stdout |
| `--format <format>` | Output format: `json` or `text` | `text` |
| `--ocr-server-url <url>` | HTTP OCR server URL | (uses Tesseract) |
| `--no-ocr` | Disable OCR entirely | enabled |
| `--ocr-language <lang>` | OCR language code | `en` |
| `--max-pages <n>` | Maximum pages to parse | `1000` |
| `--target-pages <pages>` | Specific pages (e.g., "1-5,10") | all |
| `--dpi <dpi>` | Render resolution | `150` |
| `--no-precise-bbox` | Disable bounding boxes | enabled |
| `--skip-diagonal-text` | Skip diagonal/rotated text | false |
| `--preserve-small-text` | Keep very small text | false |
| `--config <file>` | Load config from JSON file | - |
| `-q, --quiet` | Suppress progress output | false |

**Examples:**
```bash
# Basic text extraction
liteparse parse document.pdf

# JSON output with OCR disabled
liteparse parse document.pdf --format json --no-ocr

# Parse specific pages
liteparse parse document.pdf --target-pages "1-5,10,15-20"

# Use external OCR server
liteparse parse document.pdf --ocr-server-url http://localhost:5000/ocr

# Save to file
liteparse parse document.pdf -o output.txt
```

---

### `liteparse screenshot <file>`
Generate page screenshots.

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output-dir <dir>` | Output directory | `./screenshots` |
| `--pages <pages>` | Page numbers (e.g., "1,3,5" or "1-5") | all |
| `--dpi <dpi>` | Render resolution | `150` |
| `--format <format>` | Image format: `png` or `jpg` | `png` |
| `--config <file>` | Load config from JSON file | - |
| `-q, --quiet` | Suppress progress output | false |

**Examples:**
```bash
# All pages as PNG
liteparse screenshot document.pdf

# Specific pages as JPG at 300 DPI
liteparse screenshot document.pdf --pages "1,3,5" --format jpg --dpi 300

# Custom output directory
liteparse screenshot document.pdf -o ./my-screenshots
```

---

## Configuration File

Both commands accept `--config <file>` to load settings from JSON:

```json
{
  "ocrEnabled": true,
  "ocrLanguage": "en",
  "ocrServerUrl": "http://localhost:5000/ocr",
  "maxPages": 100,
  "dpi": 200,
  "outputFormat": "json",
  "preciseBoundingBox": true
}
```

CLI options override config file values.

---

## Output Behavior

- **Progress messages** go to stderr (visible in terminal)
- **Parsed content** goes to stdout (can be piped)
- Use `-o` to save to file instead of stdout
- Use `-q` to suppress all progress messages

**Piping example:**
```bash
# Extract and search
liteparse parse document.pdf -q | grep "keyword"

# Chain with other tools
liteparse parse document.pdf --format json -q | jq '.pages[0].text'
```

---

## Adding CLI Options

1. Add `.option()` call in the command definition
2. Read option in action handler from `options` object
3. Add to config object that's passed to `LiteParse`
4. If new config field, update `src/core/types.ts` and `src/core/config.ts`
