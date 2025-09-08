from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hybrid_llama_deepseek import model_manager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/models', methods=['GET'])
def get_models():
    """Get available models"""
    try:
        models = model_manager.get_available_models()
        return jsonify({'success': True, 'models': models})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    """Generate text using selected model(s)"""
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 50)
    temperature = data.get('temperature', 1.0)
    model_type = data.get('model_type', 'llama')  # 'llama', 'deepseek', or 'both'
    
    try:
        if model_type in ['llama', 'deepseek']:
            result = model_manager.generate_with_model(
                prompt, model_type, max_tokens, temperature
            )
            return jsonify({
                'success': True, 
                'result': result,
                'model_used': model_type
            })
        elif model_type == 'both':
            results = model_manager.hybrid_generate(
                prompt, max_tokens, temperature, 'both'
            )
            return jsonify({
                'success': True, 
                'results': results,
                'model_used': 'both'
            })
        else:
            return jsonify({
                'success': False, 
                'error': f'Invalid model type: {model_type}'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/compare', methods=['POST'])
def compare():
    """Compare outputs from both models"""
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 50)
    temperature = data.get('temperature', 1.0)
    
    try:
        results = model_manager.hybrid_generate(
            prompt, max_tokens, temperature, 'both'
        )
        return jsonify({
            'success': True, 
            'comparison': results
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)