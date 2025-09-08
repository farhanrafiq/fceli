import sys
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HybridModelManager:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.load_models()
    
    def load_models(self):
        """Load both Llama and DeepSeek models"""
        # Llama model (using DialoGPT as an open alternative)
        llama_model_name = "microsoft/DialoGPT-medium"
        try:
            logger.info(f"Loading Llama model: {llama_model_name}")
            self.tokenizers['llama'] = AutoTokenizer.from_pretrained(llama_model_name)
            self.models['llama'] = AutoModelForCausalLM.from_pretrained(llama_model_name)
            if self.tokenizers['llama'].pad_token is None:
                self.tokenizers['llama'].pad_token = self.tokenizers['llama'].eos_token
            logger.info("Llama model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Llama model: {e}")
        
        # DeepSeek model (using GPT-2 as a proxy since actual DeepSeek may not be public)
        deepseek_model_name = "gpt2-medium"
        try:
            logger.info(f"Loading DeepSeek model: {deepseek_model_name}")
            self.tokenizers['deepseek'] = AutoTokenizer.from_pretrained(deepseek_model_name)
            self.models['deepseek'] = AutoModelForCausalLM.from_pretrained(deepseek_model_name)
            if self.tokenizers['deepseek'].pad_token is None:
                self.tokenizers['deepseek'].pad_token = self.tokenizers['deepseek'].eos_token
            logger.info("DeepSeek model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading DeepSeek model: {e}")

    def deepseek_sample(self, logits, temperature: float = 1.0):
        """DeepSeek-V3 style sampling"""
        logits = logits / max(temperature, 1e-5)
        probs = torch.softmax(logits, dim=-1)
        return probs.div_(torch.empty_like(probs).exponential_(1)).argmax(dim=-1)

    def generate_with_model(self, prompt: str, model_type: str = "llama", 
                          max_new_tokens: int = 50, temperature: float = 1.0) -> str:
        """Generate text using specified model"""
        if model_type not in self.models:
            raise ValueError(f"Model {model_type} not available. Available models: {list(self.models.keys())}")
        
        model = self.models[model_type]
        tokenizer = self.tokenizers[model_type]
        
        # Tokenize input
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        output_ids = input_ids.clone()
        
        model.eval()
        with torch.no_grad():
            for _ in range(max_new_tokens):
                outputs = model(output_ids)
                logits = outputs.logits[:, -1, :]
                
                # Use DeepSeek sampling for both models for consistency
                next_token = self.deepseek_sample(logits, temperature)
                output_ids = torch.cat([output_ids, next_token.unsqueeze(0)], dim=1)
                
                # Stop if we hit the end token
                if next_token.item() == tokenizer.eos_token_id:
                    break
        
        # Decode the full sequence
        generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return generated_text

    def hybrid_generate(self, prompt: str, max_new_tokens: int = 50, 
                       temperature: float = 1.0, model_mix: str = "both") -> Dict:
        """Generate text using hybrid approach"""
        results = {}
        
        if model_mix == "both" or model_mix == "llama":
            try:
                results['llama'] = self.generate_with_model(
                    prompt, "llama", max_new_tokens, temperature
                )
            except Exception as e:
                results['llama'] = f"Error: {str(e)}"
        
        if model_mix == "both" or model_mix == "deepseek":
            try:
                results['deepseek'] = self.generate_with_model(
                    prompt, "deepseek", max_new_tokens, temperature
                )
            except Exception as e:
                results['deepseek'] = f"Error: {str(e)}"
        
        return results

    def get_available_models(self) -> list:
        """Get list of available models"""
        return list(self.models.keys())

# Global model manager instance
model_manager = HybridModelManager()

# Backward compatibility functions
def hybrid_generate(prompt, max_new_tokens=50, temperature=1.0):
    """Backward compatibility function"""
    results = model_manager.hybrid_generate(prompt, max_new_tokens, temperature)
    if 'llama' in results:
        return results['llama']
    elif 'deepseek' in results:
        return results['deepseek']
    else:
        return "No models available"

if __name__ == "__main__":
    prompt = "Hello, how can I help you today?"
    print("Hybrid Model Output:")
    print(hybrid_generate(prompt))
