# backend/app.py
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import uvicorn

MODEL_DIR = os.environ.get("MODEL_DIR", "gpt2")  # Load base GPT2 from HF
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

app = FastAPI(title="ProDigy GPT-2 Inference API")

# -------------------- CORS --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Request Model --------------------
class GenRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 150
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    num_return_sequences: Optional[int] = 1

# -------------------- Load Model --------------------
@app.on_event("startup")
def load_model():
    global tokenizer, model
    print(f"Loading model: {MODEL_DIR}")
    
    tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    model = AutoModelForCausalLM.from_pretrained(MODEL_DIR)

    model.to(DEVICE)
    model.eval()

# -------------------- Generate Endpoint --------------------
@app.post("/generate")
def generate_text(req: GenRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt must be a non-empty string.")

    input_ids = tokenizer(req.prompt, return_tensors="pt").input_ids.to(DEVICE)

    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            do_sample=True,
            max_length=req.max_length + input_ids.shape[-1],
            temperature=req.temperature,
            top_p=req.top_p,
            num_return_sequences=req.num_return_sequences,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    responses = []
    for output in outputs:
        gen = tokenizer.decode(output[input_ids.shape[-1]:], skip_special_tokens=True)
        responses.append(gen.strip())

    return {"prompt": req.prompt, "responses": responses}

# -------------------- Root Endpoint --------------------
@app.get("/")
def root():
    return {"status": "ok", "model": MODEL_DIR, "device": DEVICE}

# -------------------- Run App --------------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
