# 1. Base image
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip wheel==0.46.2 jaraco.context==6.1.0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# 7. Run application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]