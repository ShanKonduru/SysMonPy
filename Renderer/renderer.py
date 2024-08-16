import matplotlib.pyplot as plt
import psycopg2
from datetime import datetime

def fetch_data():
    conn = psycopg2.connect("dbname=monitoring_db user=user password=password host=localhost")
    cursor = conn.cursor()
    query = "SELECT timestamp, cpu_usage, memory_usage, ram_usage, disk_usage, disk_space FROM system_data"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def plot_data(data):
    timestamps = [datetime.fromisoformat(row[0]) for row in data]
    cpu_usage = [row[1] for row in data]
    memory_usage = [row[2] for row in data]
    ram_usage = [row[3] for row in data]
    disk_usage = [row[4] for row in data]
    disk_space = [row[5] for row in data]

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 2, 1)
    plt.plot(timestamps, cpu_usage, label='CPU Usage')
    plt.xlabel('Time')
    plt.ylabel('CPU Usage (%)')
    plt.legend()

    plt.subplot(2, 2, 2)
    plt.plot(timestamps, memory_usage, label='Memory Usage', color='r')
    plt.xlabel('Time')
    plt.ylabel('Memory Usage (%)')
    plt.legend()

    plt.subplot(2, 2, 3)
    plt.plot(timestamps, ram_usage, label='RAM Usage', color='g')
    plt.xlabel('Time')
    plt.ylabel('RAM Usage (Bytes)')
    plt.legend()

    plt.subplot(2, 2, 4)
    plt.plot(timestamps, disk_usage, label='Disk Usage', color='b')
    plt.xlabel('Time')
    plt.ylabel('Disk Usage (%)')
    plt.legend()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    data = fetch_data()
    plot_data(data)
