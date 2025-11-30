# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy code
COPY . .

EXPOSE 8000

ENV MODEL_DIR=/app/outputs/gpt2-finetuned
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
