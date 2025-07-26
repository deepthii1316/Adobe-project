FROM python:3.9-slim

WORKDIR /app

# Install system dependencies (if needed for future OCR support)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the extraction script
COPY extract_headings.py .

# Set input/output directories
RUN mkdir -p /app/input /app/output

# Run the script
CMD ["python", "extract_headings.py"]
