import fitz  # PyMuPDF
import os
import json

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = set()
    text_spans = []

    # Extract all text spans with their font info
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        for b in blocks:
            if "lines" in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if len(text) < 2:
                            continue
                        font_sizes.add(s["size"])
                        text_spans.append({
                            "text": text,
                            "size": s["size"],
                            "font": s["font"],
                            "flags": s["flags"],
                            "page": page_num + 1
                        })

    # Sort font sizes descending (largest first)
    sorted_sizes = sorted(font_sizes, reverse=True)

    if len(sorted_sizes) == 0:
        # No text found
        return {"title": "", "outline": []}

    title = ""
    outline = []

    # Assign heading sizes:
    # The largest font on first page is Title
    # Next biggest font sizes assigned as H1, H2, H3 in order
    heading_sizes = sorted_sizes[1:4]  # next up to 3 font sizes

    for span in text_spans:
        size = span["size"]
        text = span["text"]
        page = span["page"]
        flags = span["flags"]

        # Title detection: largest font on page 1
        if size == sorted_sizes[0] and page == 1:
            title = text
            continue

        # Check for headings based on font size (ignoring bold filtering for robustness)
        if size in heading_sizes:
            level_index = heading_sizes.index(size)
            level = f"H{level_index + 1}"

            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    # Remove duplicate headings (if any) preserving order
    seen = set()
    filtered_outline = []
    for h in outline:
        key = (h["level"], h["text"], h["page"])
        if key not in seen:
            filtered_outline.append(h)
            seen.add(key)

    return {
        "title": title,
        "outline": filtered_outline
    }

if __name__ == "__main__":
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    for fname in os.listdir(input_dir):
        if fname.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_dir, fname)
            print(f"Processing {fname}...")
            result = extract_outline(pdf_path)

            json_name = fname.rsplit(".", 1)[0] + ".json"
            with open(os.path.join(output_dir, json_name), "w") as f:
                json.dump(result, f, indent=2)

            print(f"Output saved to {json_name}")
