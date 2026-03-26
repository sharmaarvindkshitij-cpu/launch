from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils.analyzer import analyze_message, analyze_url, analyze_upi
from utils.db import init_db, save_scan, get_recent_scans
import os

app = Flask(__name__)

# Initialize DB
init_db()

# Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
@limiter.limit("10 per minute")
def analyze():
    data = request.json
    if not data or 'type' not in data or 'content' not in data:
        return jsonify({"error": "Invalid request format. Required: type, content"}), 400
        
    scan_type = data.get('type', '').strip().lower()
    
    # Alias mapping for improved robustness
    if scan_type in ['sms', 'email']:
        scan_type = 'message'
        
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({"error": "Content cannot be empty"}), 400
        
    if scan_type == 'message':
        result = analyze_message(content)
    elif scan_type == 'url':
        is_deep_scan = data.get('deep_scan', False)
        if is_deep_scan:
            from utils.url_scanner import DeepURLScanner
            scanner = DeepURLScanner(content)
            result = scanner.run_scan()
        else:
            result = analyze_url(content)
    elif scan_type == 'upi':
        result = analyze_upi(content)
    else:
        return jsonify({"error": "Invalid scan type. Must be message, url, or upi"}), 400
        
    # Save to history
    save_scan(scan_type, content, result)
    
    return jsonify(result)

@app.route('/history', methods=['GET'])
def history():
    limit = request.args.get('limit', default=10, type=int)
    results = get_recent_scans(limit)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
