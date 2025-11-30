Prodigy GPT-2 Backend – README
📌 Overview

This backend provides the API for running GPT-2 text generation and supporting Prodigy-based annotation workflows using FastAPI.

🚀 Features

FastAPI backend

GPT-2 text generation API (/generate)

Clean, modular structure

Easy to extend for training or annotation

📂 Project Structure
backend/
│── app/
│   ├── main.py
│   ├── gpt2_model.py
│   ├── config.py
│── models/
│── requirements.txt
└── readme_backend.md

⚙️ Installation

Install all dependencies:

pip install -r requirements.txt

▶️ Running the Backend

Start the FastAPI server:

uvicorn app.main:app --reload


Server runs on:

http://127.0.0.1:8000

🧠 API Endpoint
POST /generate

Generate text using GPT-2.

Request:
{
  "prompt": "Agriculture in India",
  "max_length": 50
}

Response:
{
  "generated_text": "Agriculture in India..."
}

