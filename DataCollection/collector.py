import psutil
import requests
import time
import socket
from datetime import datetime

REST_SERVICE_URL = 'http://localhost:5000/data'

def get_system_metrics():
    return {
        'cpu_usage': psutil.cpu_percent(),
        'memory_usage': psutil.virtual_memory().percent,
        'ram_usage': psutil.virtual_memory().available,
        'disk_usage': psutil.disk_usage('/').percent,
        'disk_space': psutil.disk_usage('/').free,
    }

def send_metrics():
    metrics = get_system_metrics()
    metrics['ip_address'] = socket.gethostbyname(socket.gethostname())
    metrics['timestamp'] = datetime.now().isoformat()
    
    response = requests.post(REST_SERVICE_URL, json=metrics)
    if response.status_code != 200:
        print(f"Failed to send data: {response.text}")

if __name__ == "__main__":
    while True:
        send_metrics()
        time.sleep(3600)  # Sleep for 1 hour
