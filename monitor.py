from flask import Flask, jsonify
import time
import socket
import psutil
import os
import random
import json

app = Flask(__name__)

# Configuration
config = {
    'site_url': 'phonoverse.x10.bz',
    'check_interval': 30,
    'ping_timeout': 1,
    'log_file': 'monitor_log.json',
    'locations': {
        'NA': 'North America',
        'EU': 'Europe',
        'AS': 'Asia'
    }
}

def check_server_status(host):
    metrics = {}
    
    # Basic connection check
    start_time = time.time()
    try:
        s = socket.create_connection((host, 80), config['ping_timeout'])
        s.close()
        response_time = (time.time() - start_time) * 1000
        metrics['status'] = 1
    except socket.error:
        response_time = 0
        metrics['status'] = 0
    
    metrics['response_time'] = round(response_time, 2)
    metrics['memory_usage'] = psutil.virtual_memory().used
    metrics['cpu_load'] = psutil.cpu_percent()
    metrics['disk_usage'] = psutil.disk_usage('/').percent

    # Simulated regional latency
    metrics['regional_latency'] = {
        'NA': round(metrics['response_time'] * (1 + random.uniform(-0.2, 0.2)), 2),
        'EU': round(metrics['response_time'] * (1 + random.uniform(-0.2, 0.2)), 2),
        'AS': round(metrics['response_time'] * (1 + random.uniform(-0.2, 0.2)), 2)
    }
    
    return metrics

def log_status(data):
    log_data = []
    if os.path.exists(config['log_file']):
        with open(config['log_file'], 'r') as log_file:
            log_data = json.load(log_file)
    
    log_data.append({**data, 'timestamp': time.time()})
    log_data = [entry for entry in log_data if entry['timestamp'] > (time.time() - 86400)]  # Keep only last 24 hours
    
    with open(config['log_file'], 'w') as log_file:
        json.dump(log_data, log_file)
    
    return log_data

def calculate_uptime(log_data):
    if not log_data:
        return 0
    up_count = sum(1 for entry in log_data if entry['status'] == 1)
    return round((up_count / len(log_data)) * 100, 2)

@app.route('/status', methods=['GET'])
def get_status():
    result = check_server_status(config['site_url'])
    log_data = log_status(result)
    uptime = calculate_uptime(log_data)
    
    response = {
        'current_status': result,
        'uptime': uptime,
        'log_data': log_data[-10:]  # Return the last 10 records for charting
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
