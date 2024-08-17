import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import psycopg2
from datetime import datetime
import numpy as np

DB_LOCATION = 'LOCAL' # 'CLOUD' # 

def fetch_data(query):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def calculate_limits(values):
    mean = np.mean(values)
    sigma = np.std(values)
    ucl = mean + 3 * sigma
    lcl = mean - 3 * sigma
    return mean, ucl, lcl

def plot_data(data, ax, ylabel):
    timestamps = [datetime.fromisoformat(row[0]) for row in data]
    values = [row[1] for row in data]
    
    # Calculate control limits
    mean, ucl, lcl = calculate_limits(values)

    # Plot the data
    ax.plot(timestamps, values, label='Data')
    ax.axhline(mean, color='gray', linestyle='--', label='Mean')
    ax.axhline(ucl, color='red', linestyle='--', label='UCL (Mean + 3 Sigma)')
    ax.axhline(lcl, color='blue', linestyle='--', label='LCL (Mean - 3 Sigma)')
    
    ax.set_xlabel('Time')
    ax.set_ylabel(ylabel)
    ax.legend()
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

        # Add the navigation toolbar
        toolbar = NavigationToolbar2Tk(canvas, tab)
        toolbar.update()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

    tab_control.pack(expand=1, fill="both")

    def on_closing():
        root.quit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    if (DB_LOCATION == 'CLOUD'):
        DATABASE_URL = "postgresql://app:8nQw8Tn3Zi10yK7PL1a40a3E@partly-complete-lioness.a1.pgedge.io/monitoring_db?sslmode=require"
    else:
        DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/monitoring_db'

    create_tabbed_interface()
