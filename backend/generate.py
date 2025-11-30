# backend/generate.py
import argparse
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def generate(model_dir, prompt, max_length=150, temperature=0.7, top_p=0.9, num_return_sequences=1):
    tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_dir)
    model.eval()
    if torch.cuda.is_available():
        model.to("cuda")

    # prepare input
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids
    if torch.cuda.is_available():
        input_ids = input_ids.to("cuda")

    outputs = model.generate(
        input_ids=input_ids,
        do_sample=True,
        max_length=max_length + input_ids.shape[-1],
        temperature=temperature,
        top_p=top_p,
        top_k=0,
        num_return_sequences=num_return_sequences,
        pad_token_id=tokenizer.pad_token_id
    )

    results = [tokenizer.decode(o[input_ids.shape[-1]:], skip_special_tokens=True) for o in outputs]
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", type=str, default="./outputs/gpt2-finetuned")
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--max_length", type=int, default=150)
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    out = generate(args.model_dir, args.prompt, max_length=args.max_length, temperature=args.temperature)
    print("=== Generation ===")
    for o in out:
        print(o)
