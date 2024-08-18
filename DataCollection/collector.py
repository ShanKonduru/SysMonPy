import psutil
import requests
import time
import socket
from datetime import datetime

REST_SERVICE_URL = 'http://192.168.127.163:5000/data'

def get_system_metrics():
    print('in get_system_metrics')
    return {
        'cpu_usage': psutil.cpu_percent(),
        'memory_usage': psutil.virtual_memory().percent,
        'ram_usage': psutil.virtual_memory().available,
        'disk_usage': psutil.disk_usage('/').percent,
        'disk_space': psutil.disk_usage('/').free,
    }

def send_metrics():
    print('in send_metrics()')
    metrics = get_system_metrics()
    print('getting ip address')
    metrics['ip_address'] = socket.gethostbyname(socket.gethostname())
    print('getting time stamp')
    metrics['timestamp'] = datetime.now().isoformat()
    print('calling REST API')
    response = requests.post(REST_SERVICE_URL, json=metrics)
    print(metrics)

    if response.status_code != 200:
        print(f"Failed to send data: {response.text}")

if __name__ == "__main__":
    cycle = 1
    while True:
        print(cycle)
        send_metrics()
        time.sleep(10)  # Sleep for 1 hour put 3600
        cycle= cycle+1
