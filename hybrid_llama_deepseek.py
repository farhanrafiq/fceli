import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# --- Load Llama model (Hugging Face style) ---
llama_model_name = "microsoft/DialoGPT-medium"  # Using an open model for demonstration
try:
    llama_tokenizer = AutoTokenizer.from_pretrained(llama_model_name)
    llama_model = AutoModelForCausalLM.from_pretrained(llama_model_name)
except Exception as e:
    print(f"Error loading Llama model: {e}")
    sys.exit(1)

# --- DeepSeek-V3 style sampling (from generate.py) ---
def deepseek_sample(logits, temperature: float = 1.0):
    logits = logits / max(temperature, 1e-5)
    probs = torch.softmax(logits, dim=-1)
    return probs.div_(torch.empty_like(probs).exponential_(1)).argmax(dim=-1)

# --- Hybrid generation function ---
def hybrid_generate(prompt, max_new_tokens=50, temperature=1.0):
    input_ids = llama_tokenizer(prompt, return_tensors="pt").input_ids
    output_ids = input_ids.clone()
    llama_model.eval()
    with torch.no_grad():
        for _ in range(max_new_tokens):
            logits = llama_model(output_ids).logits[:, -1, :]
            next_token = deepseek_sample(logits, temperature)
            output_ids = torch.cat([output_ids, next_token.unsqueeze(0)], dim=1)
            if next_token.item() == llama_tokenizer.eos_token_id:
                break
    return llama_tokenizer.decode(output_ids[0], skip_special_tokens=True)

if __name__ == "__main__":
    prompt = "Hello, how can I help you today?"
    print("Hybrid Model Output:")
    print(hybrid_generate(prompt))
