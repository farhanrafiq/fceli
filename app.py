from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hybrid_llama_deepseek import hybrid_generate

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt', '')
    max_tokens = data.get('max_tokens', 50)
    temperature = data.get('temperature', 1.0)
    
    try:
        result = hybrid_generate(prompt, max_new_tokens=max_tokens, temperature=temperature)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)