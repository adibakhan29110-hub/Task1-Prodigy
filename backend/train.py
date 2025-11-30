# backend/train.py
"""
Fine-tune GPT-2 for causal language modelling on JSONL prompt/completion pairs.

Dataset format (JSONL):
{"prompt": "Question: ...\nAnswer:", "completion": " The answer text ..."}
Each line is a JSON object. For training we concatenate prompt + completion as a single sequence
and let the model predict the whole sequence (or optionally mask the prompt tokens out of the loss).

Usage examples:
python train.py --train_file data/train.jsonl --valid_file data/val.jsonl --output_dir ./outputs/gpt2-finetuned --model_name gpt2 --epochs 3 --batch_size 2 --lr 5e-5
"""

import argparse
import os
from typing import Dict

import torch
from datasets import load_dataset, Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    DataCollatorForLanguageModeling,
    set_seed,
)

def prepare_dataset(train_file, valid_file, tokenizer, max_length=512):
    # Load JSONL where each item has "prompt" and "completion"
    data_files = {}
    if train_file:
        data_files["train"] = train_file
    if valid_file:
        data_files["validation"] = valid_file

    ds = load_dataset("json", data_files=data_files)

    def concat_example(example: Dict):
        # Join prompt + completion with a special separator if needed
        prompt = example.get("prompt", "")
        completion = example.get("completion", "")
        text = prompt + completion
        return {"text": text}

    ds = ds.map(concat_example, remove_columns=ds["train"].column_names if "train" in ds else None)
    # Tokenize
    def tokenize(examples):
        return tokenizer(examples["text"], truncation=True, max_length=max_length)
    ds = ds.map(tokenize, batched=True, remove_columns=["text"])
    return ds

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train_file", type=str, help="Path to train JSONL", required=True)
    parser.add_argument("--valid_file", type=str, help="Path to val JSONL", required=False)
    parser.add_argument("--model_name", type=str, default="gpt2", help="Pretrained model name")
    parser.add_argument("--output_dir", type=str, default="./outputs/gpt2-finetuned")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=2)
    parser.add_argument("--lr", type=float, default=5e-5)
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--fp16", action="store_true", help="Use fp16")
    args = parser.parse_args()

    set_seed(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    # Ensure model has pad token (gpt2 doesn't by default)
    if tokenizer.pad_token is None:
        tokenizer.add_special_tokens({"pad_token": "<|pad|>"})

    model = AutoModelForCausalLM.from_pretrained(args.model_name)
    model.resize_token_embeddings(len(tokenizer))

    print("Preparing dataset...")
    ds = prepare_dataset(args.train_file, args.valid_file, tokenizer, max_length=args.max_length)

    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        num_train_epochs=args.epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        evaluation_strategy="steps" if args.valid_file else "no",
        eval_steps=500,
        logging_steps=100,
        save_strategy="steps",
        save_steps=500,
        learning_rate=args.lr,
        weight_decay=0.01,
        warmup_steps=100,
        fp16=args.fp16,
        gradient_accumulation_steps=max(1, 8 // args.batch_size),
        push_to_hub=False,
        report_to=["wandb"] if "WANDB_API_KEY" in os.environ else None,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=ds["train"],
        eval_dataset=ds["validation"] if "validation" in ds else None,
        data_collator=data_collator,
    )

    trainer.train()
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print("Training complete. Model saved to:", args.output_dir)

if __name__ == "__main__":
    main()

