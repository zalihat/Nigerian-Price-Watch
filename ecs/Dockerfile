# Use Python 3.10 base image (lighter and not tied to Lambda)
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --only-binary=:all: pyarrow \
    && pip install -r requirements.txt

# Copy your application code
COPY clean_data.py .

# Default command: run your main script
CMD ["python", "clean_data.py"]

