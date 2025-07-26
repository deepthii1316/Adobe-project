import fitz
import os
import json

def extract_outline(pdf_path):
    doc = fitz.open(pdf_path)
    font_sizes = set()
    line_info = []

    # Collect full lines, grouping concatenated span texts
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for l in b["lines"]:
                line_text = ""
                sizes = []
                fonts = []
                flags_list = []
                spans = l["spans"]

                for s in spans:
                    t = s["text"].strip()
                    if not t:
                        continue
                    line_text += t + " "
                    sizes.append(s["size"])
                    fonts.append(s["font"])
                    flags_list.append(s["flags"])

                line_text = line_text.strip()
                if not line_text or len(line_text) < 2:
                    continue

                # Use main span attributes (first span) as representative
                font_sizes.add(sizes[0])
                line_info.append({
                    "text": line_text,
                    "size": sizes[0],
                    "font": fonts[0],
                    "flags": flags_list[0],
                    "page": page_num + 1
                })

    if not font_sizes:
        return {"title": "", "outline": []}

    sorted_sizes = sorted(font_sizes, reverse=True)
    title = ""
    outline = []
    heading_sizes = sorted_sizes[1:4]

    for item in line_info:
        size = item["size"]
        text = item["text"]
        page = item["page"]
        flags = item["flags"]

        # Title
        if size == sorted_sizes[0] and page == 1:
            title = text
            continue
        # Headings (require minimum length, not ending with a dot, and bold)
        if size in heading_sizes:
            if not (flags & 2):
                continue
            if len(text) < 4 or text.endswith('.'):
                continue
            level_index = heading_sizes.index(size)
            level = f"H{level_index + 1}"
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    # Deduplicate
    seen = set()
    filtered_outline = []
    for h in outline:
        key = (h["level"], h["text"], h["page"])
        if key not in seen:
            filtered_outline.append(h)
            seen.add(key)

    return {"title": title, "outline": filtered_outline}

# The main() function and usage remain the same.


def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDFs found in input/")
        return

    for fname in pdf_files:
        pdf_path = os.path.join(input_dir, fname)
        print(f"Processing {fname} ...")
        result = extract_outline(pdf_path)

        json_name = fname.rsplit(".", 1)[0] + ".json"
        json_path = os.path.join(output_dir, json_name)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Output saved to {json_name}")


if __name__ == "__main__":
    main()
