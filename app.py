from flask import Flask, request, jsonify
import os
from functools import wraps
from audio_sync import AudioSyncProcessor

app = Flask(__name__)

# Initialize the audio sync processor
sync_processor = AudioSyncProcessor()

# Protected endpoints that require API key
PROTECTED_ENDPOINTS = ['/sync']

@app.before_request
def check_api_key():
    """Middleware to check API key for protected endpoints."""
    # Skip API key check for health endpoint and root
    if request.endpoint in ['health_check', 'index']:
        return None
    
    # Check if this is a protected endpoint
    if request.path in PROTECTED_ENDPOINTS:
        api_key = request.headers.get('APIKEY')
        expected_key = os.environ.get('APIKEY')
        
        if not expected_key:
            return None
            return jsonify({'error': 'API key not configured on server'}), 500
        
        if not api_key:
            return jsonify({'error': 'APIKEY header required'}), 401
        
        if api_key != expected_key:
            return jsonify({'error': 'Invalid API key'}), 401
    
    # API key is valid or endpoint is not protected
    return None

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'audio-sync-api'})

@app.route('/sync', methods=['POST'])
def sync_audio():
    """
    Sync two audio files using file paths.
    
    Expected JSON payload:
    {
        "reference_file": "/path/to/reference.wav",
        "target_file": "/path/to/target.wav"
    }
    
    Returns:
    JSON with sync results
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON payload required'}), 400
        
        reference_file = data.get('reference_file')
        target_file = data.get('target_file')
        
        if not reference_file or not target_file:
            return jsonify({'error': 'Both reference_file and target_file are required'}), 400
        
        # Perform sync using the processor
        result = sync_processor.sync_files(reference_file, target_file)
        
        if result['success']:
            return jsonify({'offset': result['offset_seconds']})
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Simple API documentation."""
    return jsonify({
        'service': 'Audio Sync API',
        'version': '2.0',
        'endpoints': {
            'POST /sync': 'Sync two audio files using file paths (requires APIKEY header)',
            'GET /health': 'Health check'
        },
        'supported_formats': list(sync_processor.supported_formats),
        'authentication': 'Required: APIKEY header for /sync endpoint',
        'usage': {
            'sync': {
                'method': 'POST',
                'content_type': 'application/json',
                'headers': {
                    'APIKEY': 'your-api-key'
                },
                'payload': {
                    'reference_file': '/path/to/reference.wav',
                    'target_file': '/path/to/target.wav'
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
