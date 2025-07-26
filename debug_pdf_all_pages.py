
import fitz  # PyMuPDF
import os
import json

def debug_pdf_extraction(pdf_path):
    """Debug function to see what's actually being extracted from the PDF"""
    print(f"\n=== DEBUGGING: {pdf_path} ===")

    doc = fitz.open(pdf_path)
    print(f"Number of pages: {len(doc)}")

    all_text = ""
    font_sizes = set()

    for page_num in range(min(2, len(doc))):  # Check first 2 pages only
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]

        print(f"\nPage {page_num + 1}:")
        print(f"Number of blocks: {len(blocks)}")

        for block_num, b in enumerate(blocks):
            if "lines" not in b:
                continue

            for line_num, line in enumerate(b["lines"]):
                line_text = ""
                for span in line["spans"]:
                    text = span["text"].strip()
                    if text:
                        line_text += text + " "
                        font_sizes.add(span["size"])
                        all_text += text + " "

                line_text = line_text.strip()
                if line_text and len(line_text) > 2:
                    print(f"  Line {line_num}: '{line_text}' (size: {line['spans'][0]['size'] if line['spans'] else 'N/A'})")

    print(f"\nAll font sizes found: {sorted(font_sizes, reverse=True)}")
    print(f"Total text characters: {len(all_text)}")
    print(f"First 200 characters: {all_text[:200]}...")

    return len(all_text) > 0

def main():
    input_dir = "input"

    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' not found!")
        return

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in input directory!")
        return

    print(f"Found {len(pdf_files)} PDF files:")
    for i, fname in enumerate(pdf_files[:3]):  # Debug first 3 PDFs only
        print(f"{i+1}. {fname}")
        try:
            pdf_path = os.path.join(input_dir, fname)
            has_text = debug_pdf_extraction(pdf_path)
            print(f"Has extractable text: {has_text}")
        except Exception as e:
            print(f"Error processing {fname}: {e}")

if __name__ == "__main__":
    main()
