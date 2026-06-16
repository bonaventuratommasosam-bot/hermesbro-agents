# PDF Text Extraction

Extract text from PDFs using PyMuPDF (fitz).

## Installation

```bash
python3 -m venv pdf-venv
source pdf-venv/bin/activate
pip install pymupdf
```

## Basic Usage

```python
import fitz  # PyMuPDF

doc = fitz.open("document.pdf")
print(f"Pages: {len(doc)}")

# Extract text from all pages
full_text = ""
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    full_text += f"\n--- Page {page_num + 1} ---\n{text}"
```

## Extract Specific Pages

```python
# Extract pages 5-12
for page_num in range(4, 12):  # 0-indexed
    page = doc[page_num]
    text = page.get_text()
    print(f"Page {page_num + 1}: {text[:500]}")
```

## Save Extracted Text

```python
with open("output.txt", "w") as f:
    f.write(full_text)
```

## Search for Sections

```python
sections = ["Introduction", "Methods", "Results", "Conclusion"]
for section in sections:
    idx = full_text.find(section)
    if idx != -1:
        print(f"[{section}] at char {idx}")
        print(full_text[idx:idx+500])
```

## Pitfalls

- PyMuPDF requires a virtual environment on systems with PEP 668 (use `python3 -m venv`)
- Large PDFs may take time to process — use page ranges for efficiency
- Some PDFs have scanned images instead of text — use OCR tools (tesseract, marker-pdf) for those
- Unicode characters may not extract cleanly from all PDFs
