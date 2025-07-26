import os
from extract_headings import extract_structure
from output_utils import save_to_json

input_dir = "input"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

for file in os.listdir(input_dir):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(input_dir, file)
        title, outline = extract_structure(pdf_path)

        json_name = file.replace(".pdf", ".json")
        output_path = os.path.join(output_dir, json_name)

        save_to_json(title, outline, output_path)
        print(f"Processed {file} → {json_name}")
