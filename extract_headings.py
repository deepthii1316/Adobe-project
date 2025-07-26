import fitz  # PyMuPDF

def extract_structure(pdf_path):
    doc = fitz.open(pdf_path)
    title = ""
    outline = []

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for line in b.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    size = span["size"]
                    font = span["font"]

                    if not text:
                        continue
                    
                    # Title = first large centered text
                    if not title and size > 15:
                        title = text
                    
                    level = None
                    if size >= 15:
                        level = "H1"
                    elif 13 <= size < 15:
                        level = "H2"
                    elif 11 <= size < 13:
                        level = "H3"
                    
                    if level:
                        outline.append({
                            "level": level,
                            "text": text,
                            "page": page_number
                        })

    return title, outline
