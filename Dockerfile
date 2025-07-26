FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your script on container startup
CMD ["python", "main.py"]
