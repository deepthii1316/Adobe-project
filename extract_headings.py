# import fitz  # PyMuPDF

# def extract_structure(pdf_path):
#     doc = fitz.open(pdf_path)
#     title = ""
#     outline = []

#     for page_number, page in enumerate(doc, start=1):
#         blocks = page.get_text("dict")["blocks"]
#         for b in blocks:
#             for line in b.get("lines", []):
#                 for span in line["spans"]:
#                     text = span["text"].strip()
#                     size = span["size"]
#                     font = span["font"]

#                     if not text:
#                         continue
                    
#                     # Title = first large centered text
#                     if not title and size > 15:
#                         title = text
                    
#                     level = None
#                     if size >= 15:
#                         level = "H1"
#                     elif 13 <= size < 15:
#                         level = "H2"
#                     elif 11 <= size < 13:
#                         level = "H3"
                    
#                     if level:
#                         outline.append({
#                             "level": level,
#                             "text": text,
#                             "page": page_number
#                         })

#     return title, outline
import fitz  # PyMuPDF
import os
import json

def concat_spans_smart(spans):
    """Smart span concatenation to prevent word splitting like 'B O O K M A R K'"""
    if not spans:
        return ""
    
    spans = sorted(spans, key=lambda s: s['bbox'][0])
    result = spans[0]['text']
    prev_x1 = spans[0]['bbox'][2]
    
    for span in spans[1:]:
        curr_x0 = span['bbox'][0]
        gap = curr_x0 - prev_x1
        
        # If gap is small, join without space (prevents letter splitting)
        if gap <= 2.0:
            result += span['text']
        else:
            result += " " + span['text']
        
        prev_x1 = span['bbox'][2]
    
    return result.strip()

def is_paragraph_text(text):
    """Filter out obvious paragraph text"""
    text = text.strip()
    
    # Too long or too short
    if len(text) < 3 or len(text) > 100:
        return True
    
    # Contains sentence patterns
    paragraph_indicators = [
        'this tutorial', 'you should', 'designed for', 'understanding of',
        'before proceeding', 'ini addition', 'furthermore', 'contains enough',
        'through practical', 'professionals who', 'well-versed with'
    ]
    
    text_lower = text.lower()
    if any(indicator in text_lower for indicator in paragraph_indicators):
        return True
    
    # Ends with period (usually sentences)
    if text.endswith('.') and len(text.split()) > 3:
        return True
    
    # URLs or emails
    if 'http://' in text or 'www.' in text or '@' in text:
        return True
    
    return False

def extract_outline(pdf_path):
    """Extract PDF outline with balanced filtering"""
    doc = fitz.open(pdf_path)
    font_sizes = set()
    lines = []
    
    # Extract all text lines
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" not in block:
                continue
            
            for line in block["lines"]:
                spans = [s for s in line["spans"] if s["text"].strip()]
                if not spans:
                    continue
                
                # Concatenate spans smartly
                text = concat_spans_smart(spans)
                if len(text) < 2:
                    continue
                
                # Get line properties
                first_span = spans[0]
                font_sizes.add(first_span["size"])
                
                lines.append({
                    "text": text,
                    "size": first_span["size"],
                    "flags": first_span["flags"],
                    "page": page_num + 1,
                    "bbox": first_span["bbox"]
                })
    
    if not lines:
        return {"title": "", "outline": []}
    
    # Sort font sizes (largest first)
    sorted_sizes = sorted(font_sizes, reverse=True)
    
    # Find title (largest font on first page, shortest text)
    title = ""
    title_candidates = []
    
    for line in lines:
        if line["page"] == 1 and line["size"] == sorted_sizes[0]:
            if not is_paragraph_text(line["text"]):
                title_candidates.append((line["text"], len(line["text"])))
    
    if title_candidates:
        # Choose shortest title candidate
        title_candidates.sort(key=lambda x: x[1])
        title = title_candidates[0][0]
    
    # Detect headings (next 3 largest font sizes)
    heading_sizes = sorted_sizes[1:4]
    outline = []
    
    for line in lines:
        text = line["text"]
        size = line["size"]
        page = line["page"]
        
        # Skip if this is the title
        if text == title:
            continue
        
        # Check if this could be a heading
        if size in heading_sizes:
            # Apply basic filtering
            if is_paragraph_text(text):
                continue
            
            # Position filter - avoid bottom of page
            y_pos = line["bbox"][1]
            if y_pos < 50:  # Bottom margin
                continue
            
            # Assign heading level
            level_index = heading_sizes.index(size)
            level = f"H{level_index + 1}"
            
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })
    
    # Remove duplicates
    seen = set()
    filtered_outline = []
    for h in outline:
        key = (h["level"], h["text"], h["page"])
        if key not in seen:
            filtered_outline.append(h)
            seen.add(key)
    
    return {"title": title, "outline": filtered_outline}

def main():
    input_dir = "input"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(input_dir):
        print("Input directory does not exist. Please create an 'input' folder and add PDF files.")
        return
    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("No PDFs found in input/")
        return
    
    for fname in pdf_files:
        pdf_path = os.path.join(input_dir, fname)
        print(f"Processing {fname}...")
        
        try:
            result = extract_outline(pdf_path)
            
            json_name = fname.rsplit(".", 1)[0] + ".json"
            json_path = os.path.join(output_dir, json_name)
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Title: {result['title']}")
            print(f"✓ Headings: {len(result['outline'])}")
            for h in result['outline'][:3]:
                print(f"  - {h['level']}: {h['text']}")
            if len(result['outline']) > 3:
                print(f"  ... and {len(result['outline'])-3} more")
            
        except Exception as e:
            print(f"✗ Error: {e}")

if __name__ == "__main__":
    main()