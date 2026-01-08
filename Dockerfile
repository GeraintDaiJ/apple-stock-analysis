FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose API port
EXPOSE 8000

# Run fetch script first, then start API
CMD ["sh", "-c", "python fetch_and_store_aapl.py && uvicorn app.api:app --host 0.0.0.0 --port 8000"]