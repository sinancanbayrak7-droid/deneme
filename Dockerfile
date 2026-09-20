FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY requirements.txt .
COPY *.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create output directories
RUN mkdir -p output/reports output/dashboards data

# Default command
CMD ["python", "main.py", "--period", "90"]
