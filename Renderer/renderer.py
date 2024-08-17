import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import psycopg2
from datetime import datetime

DB_LOCATION = 'LOCAL' # 'CLOUD' # 

def fetch_data(query):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def plot_data(data, ax, ylabel):
    timestamps = [datetime.fromisoformat(row[0]) for row in data]
    values = [row[1] for row in data]
    
    ax.plot(timestamps, values)
    ax.set_xlabel('Time')
    ax.set_ylabel(ylabel)
    ax.legend([ylabel])
    ax.xaxis_date()
    ax.tick_params(axis='x', rotation=45)

def create_tabbed_interface():
    root = tk.Tk()
    root.title("System Data Visualization")

    tab_control = ttk.Notebook(root)

    # Queries for each tab
    queries = {
        "CPU Usage": "SELECT timestamp, cpu_usage FROM system_data",
        "Memory Usage": "SELECT timestamp, memory_usage FROM system_data",
        "RAM Usage": "SELECT timestamp, ram_usage FROM system_data",
        "Disk Usage": "SELECT timestamp, disk_usage FROM system_data"
    }

    # Labels for each tab
    labels = {
        "CPU Usage": "CPU Usage (%)",
        "Memory Usage": "Memory Usage (%)",
        "RAM Usage": "RAM Usage (Bytes)",
        "Disk Usage": "Disk Usage (%)"
    }

    for tab_name, query in queries.items():
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=tab_name)

        # Fetch data and create plot
        data = fetch_data(query)
        fig, ax = plt.subplots(figsize=(10, 6))
        plot_data(data, ax, labels[tab_name])

        # Add plot to the tab
        canvas = FigureCanvasTkAgg(fig, master=tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    tab_control.pack(expand=1, fill="both")

    root.mainloop()

if __name__ == "__main__":
    if (DB_LOCATION == 'CLOUD'):
        DATABASE_URL = "postgresql://app:8nQw8Tn3Zi10yK7PL1a40a3E@partly-complete-lioness.a1.pgedge.io/monitoring_db?sslmode=require"
    else:
        DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/monitoring_db'

    create_tabbed_interface()
