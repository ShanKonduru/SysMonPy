import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import psycopg2
from datetime import datetime
import numpy as np

DB_LOCATION = 'LOCAL' # 'CLOUD' # 

def fetch_ip_addresses():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ip_address FROM system_data")
    ip_addresses = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return ip_addresses

def fetch_data(ip_address, query):
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(query, (ip_address,))
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

    # Clear the previous plot
    ax.clear()

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

def update_tabs(ip_address):
    for tab_name, query in queries.items():
        # Create or reuse the figure and axes
        if tab_name not in figures:
            fig, ax = plt.subplots(figsize=(10, 6))
            canvas = FigureCanvasTkAgg(fig, master=tabs[tab_name])
            toolbar = NavigationToolbar2Tk(canvas, tabs[tab_name])
            toolbar.update()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
            figures[tab_name] = (fig, ax, canvas)
        else:
            fig, ax, canvas = figures[tab_name]
            canvas.get_tk_widget().pack_forget()  # Remove the old canvas

        # Fetch data and update the plot
        data = fetch_data(ip_address, query)
        plot_data(data, ax, labels[tab_name])
        canvas.draw()  # Redraw the canvas
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

def on_ip_change(event):
    ip_address = ip_var.get()
    update_tabs(ip_address)

def create_tabbed_interface():
    global tabs
    global ip_var
    global figures  # Store figures and canvases to manage them

    root = tk.Tk()
    root.title("System Data Visualization")

    # Initialize the Tkinter variable
    ip_var = tk.StringVar()

    # Dropdown for IP addresses
    ip_dropdown = ttk.Combobox(root, textvariable=ip_var)
    ip_dropdown.bind("<<ComboboxSelected>>", on_ip_change)
    ip_dropdown.pack(pady=10)

    # Fetch and populate IP addresses
    ip_addresses = fetch_ip_addresses()
    ip_dropdown['values'] = ip_addresses
    if ip_addresses:
        ip_dropdown.set(ip_addresses[0])  # Set default IP address

    tab_control = ttk.Notebook(root)
    tabs = {}
    figures = {}  # Initialize a dictionary to store figure and canvas objects

    for tab_name, query in queries.items():
        tab = ttk.Frame(tab_control)
        tabs[tab_name] = tab
        tab_control.add(tab, text=tab_name)

    tab_control.pack(expand=1, fill="both")

    # Initialize tabs with data for the default IP address
    update_tabs(ip_dropdown.get())

    def on_closing():
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    if (DB_LOCATION == 'CLOUD'):
        DATABASE_URL = "" # Provide PostgreSQL Cloud DB Connection String here.
    else:
        DATABASE_URL = "" # Provide PostgreSQL local DB Connection String here.

    # Define queries and labels
    queries = {
        "CPU Usage": "SELECT timestamp, cpu_usage FROM system_data WHERE ip_address = %s",
        "Memory Usage": "SELECT timestamp, memory_usage FROM system_data WHERE ip_address = %s",
        "RAM Usage": "SELECT timestamp, ram_usage FROM system_data WHERE ip_address = %s",
        "Disk Usage": "SELECT timestamp, disk_usage FROM system_data WHERE ip_address = %s"
    }

    labels = {
        "CPU Usage": "CPU Usage (%)",
        "Memory Usage": "Memory Usage (%)",
        "RAM Usage": "RAM Usage (Bytes)",
        "Disk Usage": "Disk Usage (%)"
    }

    create_tabbed_interface()
