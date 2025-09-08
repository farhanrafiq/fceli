# Hybrid Llama-DeepSeek AI Model Project

## Overview
This project implements a hybrid AI model that combines Llama-style models with DeepSeek-V3 sampling techniques. It provides a web interface for interacting with the model through a Flask application.

## Project Architecture
- **Main Script**: `hybrid_llama_deepseek.py` - Core hybrid model implementation
- **Web Interface**: `app.py` - Flask web server providing REST API and UI
- **Frontend**: `templates/index.html` - Interactive web interface for model interaction
- **Dependencies**: Uses both Python (transformers, torch, flask) and Node.js packages

## Recent Changes (2025-09-08)
- Set up Python 3.11 and Node.js 20 environments
- Installed AI/ML dependencies: torch (CPU), transformers, flask
- Modified model to use open Microsoft DialoGPT model instead of gated Llama model
- Created web interface with parameter controls (temperature, max tokens)
- Configured workflow to serve on port 5000
- Set up deployment configuration for VM deployment

## Current State
- ✅ All dependencies installed and working
- ✅ Core model functionality tested and operational
- ✅ Web interface running successfully on port 5000
- ✅ Deployment configuration completed
- ✅ Ready for production deployment

## Usage
The web interface allows users to:
1. Enter text prompts
2. Adjust generation parameters (temperature, max tokens)
3. Generate responses using the hybrid model
4. View results in real-time

## Technical Details
- Uses Microsoft DialoGPT-medium as the base model
- Implements DeepSeek-V3 style sampling for improved text generation
- Flask server configured for all host access (0.0.0.0:5000)
- CPU-optimized PyTorch installation for compatibility