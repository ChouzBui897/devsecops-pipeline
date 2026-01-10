# 1. Base image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy requirements
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application source
COPY . .

# 6. Expose port
EXPOSE 5000

# 7. Run application
CMD ["python", "app.py"]
