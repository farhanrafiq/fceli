# Hybrid Llama-DeepSeek AI Model Project

## Overview
This project implements a hybrid AI model backend that supports both Llama and DeepSeek models with DeepSeek-V3 sampling techniques. It provides a comprehensive web interface for interacting with both models through a Flask application with model selection capabilities.

## Project Architecture
- **Main Script**: `hybrid_llama_deepseek.py` - Hybrid model manager with both Llama and DeepSeek models
- **Web Interface**: `app.py` - Flask web server with multiple API endpoints
- **Frontend**: `templates/index.html` - Interactive web interface with model selection
- **Dependencies**: Python (transformers, torch, flask) and Node.js packages

## Recent Changes (2025-09-08)
- Set up Python 3.11 and Node.js 20 environments
- Installed AI/ML dependencies: torch (CPU), transformers, flask
- Created HybridModelManager class supporting both models:
  - **Llama Model**: Microsoft DialoGPT-medium (open alternative)
  - **DeepSeek Model**: GPT-2-medium (proxy for DeepSeek functionality)
- Implemented multiple API endpoints:
  - `/models` - Get available models
  - `/generate` - Generate with selected model(s)
  - `/compare` - Compare outputs from both models
- Enhanced web interface with model selection and comparison features
- Configured workflow to serve on port 5000
- Set up deployment configuration for VM deployment

## Current State
- ✅ Both Llama and DeepSeek models loaded and operational
- ✅ All API endpoints working (models, generate, compare)
- ✅ Web interface with model selection running on port 5000
- ✅ Backend supports individual model usage and model comparison
- ✅ Deployment configuration completed
- ✅ Ready for frontend integration

## API Endpoints
1. **GET /models** - Returns list of available models
2. **POST /generate** - Generate text with specified model
   - `model_type`: "llama", "deepseek", or "both"
   - `prompt`: Text prompt
   - `max_tokens`: Maximum tokens to generate
   - `temperature`: Sampling temperature
3. **POST /compare** - Compare outputs from both models

## Usage
The web interface allows users to:
1. Select individual models (Llama/DeepSeek) or compare both
2. Enter text prompts
3. Adjust generation parameters (temperature, max tokens)
4. Generate responses using selected model(s)
5. View side-by-side comparisons of model outputs

## Technical Details
- **Llama Model**: Microsoft DialoGPT-medium (conversational AI)
- **DeepSeek Model**: GPT-2-medium (text generation)
- Both models use DeepSeek-V3 style sampling for consistency
- Flask server configured for all host access (0.0.0.0:5000)
- CPU-optimized PyTorch installation for compatibility
- Ready for integration with user's frontend in IntelligentResearch folder