import json

def save_to_json(title, outline, output_path):
    data = {
        "title": title,
        "outline": outline
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
