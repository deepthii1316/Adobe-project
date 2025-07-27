# 📄 PDF Outline Extraction

Extract document title and hierarchical headings (H1, H2, H3) from PDF files using font size heuristics.

---

## 📝 Overview

This project extracts the main title and structured outline headings from PDFs by analyzing font sizes and filtering out paragraph or irrelevant text. It outputs a JSON file with the document title and headings along with their page numbers.

---

## ✨ Features

- 🏷️ Detects document title from the largest font on the first page.
- 🏗️ Extracts headings of levels H1 and H2 based on relative font sizes.
- 🧹 Filters out paragraph texts, URLs, emails, and other noise.
- 📂 Processes all PDFs in the `input/` directory in batch.
- 💾 Saves JSON output files in the `output/` directory.

---

## ⚙️ Requirements

- Python 3.7+
- PyMuPDF (`fitz`) library

Install dependencies with:


---

## 🛠️ Setup

1. 📥 Place your PDF files inside the `input/` folder (create it if it doesn't exist).
2. 📤 Ensure the `output/` folder exists or will be created by the script.

---

## ▶️ Usage

Run the extraction script:


---

## 🛠️ Setup

1. 📥 Place your PDF files inside the `input/` folder (create it if it doesn't exist).
2. 📤 Ensure the `output/` folder exists or will be created by the script.

---

## ▶️ Usage

Run the extraction script:


For each PDF in the `input/` folder, a corresponding JSON file will be saved in `output/` containing the extracted title and outline headings.

---

## 📄 Output Format Example


---

## 🧩 Customization

- ✏️ Modify the `is_paragraph_text()` function in the script to tweak paragraph filtering heuristics.
- ⚖️ Adjust font size thresholds (`h1_size`, `h2_threshold`, `h3_threshold`) in `extract_headings.py` to suit your PDFs.

---

## 🪪 License

MIT License

---

For questions or contributions, feel free to open issues or pull requests!

Happy extracting! 🚀
