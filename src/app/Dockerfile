# 1. Base image
FROM python:3.10-slim

# 2. Create non-root user for security
RUN useradd -m -u 1000 appuser

# 3. Set working directory
WORKDIR /app

# 4. Copy requirements
COPY requirements.txt .

# 5. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application source
COPY . .

# 7. Set proper permissions
RUN chown -R appuser:appuser /app

# 8. Switch to non-root user
USER appuser

# 9. Expose port
EXPOSE 5000

# 10. Run application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]