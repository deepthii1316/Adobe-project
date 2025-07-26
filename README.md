# PDF Outline Extraction - Adobe India Hackathon Round 1A

## Overview
This solution extracts document titles and headings (H1, H2, H3) from PDF files using font size analysis and content heuristics.

## Features
- Processes all PDFs in `input/` directory
- Outputs structured JSON files to `output/` directory
- Handles multi-span headings (prevents word splitting)
- Filters out paragraph text and false positives
- Docker containerized for consistent deployment

## Usage

### Local Execution
