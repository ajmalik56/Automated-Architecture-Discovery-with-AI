"""
Automated Architecture Discovery System
Copyright (c) 2025 Abhishek Datta

Licensed under the MIT License.
See LICENSE file in the project root for full license information.

This file is part of the Automated Architecture Discovery System,
an educational project demonstrating microservices architecture discovery.
"""

"""
Mock Splunk Log Collector
HEC-compatible log collection service
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

logs_storage = []
logs_lock = threading.Lock()
LOG_FILE = 'splunk_logs.jsonl'

def save_log_to_file(log_entry):
    """Append log to file"""
    try:
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"Error saving log: {e}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "splunk-collector"}), 200

@app.route('/services/collector/event', methods=['POST'])
def collect_event():
    """Splunk HEC (HTTP Event Collector) compatible endpoint"""
    try:
        data = request.get_json()
        
        if isinstance(data, dict) and 'event' in data:
            event = data['event']
        else:
            event = data
        
        if isinstance(event, str):
            try:
                event = json.loads(event)
            except:
                pass
        
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'sourcetype': data.get('sourcetype', 'http') if isinstance(data, dict) else 'http',
            'event': event
        }
        
        with logs_lock:
            logs_storage.append(log_entry)
        
        save_log_to_file(log_entry)
        
        return jsonify({'text': 'Success', 'code': 0}), 200
    
    except Exception as e:
        return jsonify({'text': f'Error: {str(e)}', 'code': 1}), 500

@app.route('/api/search', methods=['POST'])
def search_logs():
    """Search logs by correlation ID or other criteria"""
    try:
        query = request.get_json()
        correlation_id = query.get('correlation_id')
        service = query.get('service')
        user_id = query.get('user_id')
        
        results = []
        
        with logs_lock:
            for log in logs_storage:
                event = log.get('event', {})
                
                if isinstance(event, str):
                    try:
                        event = json.loads(event)
                    except:
                        continue
                
                match = True
                if correlation_id and event.get('correlation_id') != correlation_id:
                    match = False
                if service and event.get('service') != service:
                    match = False
                if user_id and event.get('user_id') != user_id:
                    match = False
                
                if match:
                    results.append(log)
        
        return jsonify({
            'results': results,
            'count': len(results)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/trace/<correlation_id>', methods=['GET'])
def trace_request(correlation_id):
    """Trace a complete request flow by correlation ID"""
    try:
        trace = []
        
        with logs_lock:
            for log in logs_storage:
                event = log.get('event', {})
                
                if isinstance(event, str):
                    try:
                        event = json.loads(event)
                    except:
                        continue
                
                if event.get('correlation_id') == correlation_id:
                    trace.append({
                        'timestamp': log.get('timestamp'),
                        'service': event.get('service'),
                        'message': event.get('message'),
                        'endpoint': event.get('endpoint'),
                        'user_id': event.get('user_id'),
                        'level': event.get('level')
                    })
        
        trace.sort(key=lambda x: x['timestamp'])
        
        return jsonify({
            'correlation_id': correlation_id,
            'trace': trace,
            'services_involved': list(set(t['service'] for t in trace if t.get('service')))
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get statistics about collected logs"""
    try:
        with logs_lock:
            total_logs = len(logs_storage)
            
            services = set()
            correlation_ids = set()
            
            for log in logs_storage:
                event = log.get('event', {})
                if isinstance(event, str):
                    try:
                        event = json.loads(event)
                    except:
                        continue
                
                if 'service' in event:
                    services.add(event['service'])
                if 'correlation_id' in event:
                    correlation_ids.add(event['correlation_id'])
        
        return jsonify({
            'total_logs': total_logs,
            'unique_services': len(services),
            'unique_correlation_ids': len(correlation_ids),
            'services': list(services)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear', methods=['POST'])
def clear_logs():
    """Clear all logs (for testing)"""
    try:
        with logs_lock:
            logs_storage.clear()
        
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        
        return jsonify({'message': 'Logs cleared'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("SPLUNK LOG COLLECTOR")
    print("="*60)
    print("Starting on port 8088...")
    print("HEC Endpoint: http://0.0.0.0:8088/services/collector/event")
    print("Search API: http://0.0.0.0:8088/api/search")
    print("Trace API: http://0.0.0.0:8088/api/trace/<correlation_id>")
    print("Health Check: http://0.0.0.0:8088/health")
    print("="*60)
    
    # app.run(host='0.0.0.0', port=8088, debug=False)
    # Add these parameters for production
    app.run(host='0.0.0.0', port=8088, debug=False, threaded=True, use_reloader=False)