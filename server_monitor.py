import time
import socket
import json
import os
import random
import psutil

config = {
    'site_url': 'phonoverse.x10.bz',
    'check_interval': 30,  # 30 seconds
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
        socket.create_connection((host, 80), config['ping_timeout'])
        response_time = (time.time() - start_time) * 1000
        metrics['status'] = 1
    except OSError:
        metrics['status'] = 0
        response_time = 0

    metrics['response_time'] = round(response_time, 2)

    # Additional metrics
    metrics['memory_usage'] = psutil.virtual_memory().used
    metrics['cpu_load'] = psutil.getloadavg()[0]
    metrics['disk_usage'] = psutil.disk_usage('/').percent

    # Simulated ping from different locations
    metrics['regional_latency'] = {
        'NA': round(metrics['response_time'] * (1 + random.uniform(-0.2, 0.2)), 2),
        'EU': round(metrics['response_time'] * (1 + random.uniform(-0.2, 0.2)), 2),
        'AS': round(metrics['response_time'] * (1 + random.uniform(-0.2, 0.2)), 2)
    }

    return metrics

def log_status(data):
    log_data = []
    
    if os.path.exists(config['log_file']):
        with open(config['log_file'], 'r') as file:
            log_data = json.load(file)
    
    log_data.append({'timestamp': time.time(), **data})

    # Keep only last 24 hours
    log_data = [entry for entry in log_data if entry['timestamp'] > (time.time() - 86400)]
    
    with open(config['log_file'], 'w') as file:
        json.dump(log_data, file)

def main():
    while True:
        result = check_server_status(config['site_url'])
        log_status(result)
        time.sleep(config['check_interval'])

if __name__ == '__main__':
    main()
