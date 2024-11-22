import tkinter as tk
from tkinter import ttk
import socket

# Configuración de conexión al ESP32
ESP32_IP = "192.168.0.197"  # Reemplaza con la dirección IP del ESP32
ESP32_PORT = 80  # Puerto en el ESP32 que escuchará

def send_pwm_to_esp32(max_speed):
    """
    Enviar el valor de PWM máximo al ESP32.
    """
    try:
        # Crear socket y conectar al ESP32
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((ESP32_IP, ESP32_PORT))
            client_socket.sendall(max_speed.encode('utf-8'))
            print(f"Sent to ESP32: {max_speed}")
    except Exception as e:
        print(f"Error sending to ESP32: {e}")

def start_train():
    print("Train started.")

def stop_train():
    # Enviar el valor de PWM de cero al ESP32 para detener
    send_pwm_to_esp32("0")

    print("Emergency stop activated.")

def update_controls():
    max_speed = max_speed_entry.get()
    min_speed = min_speed_entry.get()
    wait_time = wait_time_entry.get()

    print(f"Max Speed: {max_speed}")
    print(f"Min Speed: {min_speed}")
    print(f"Wait Time: {wait_time}")

    # Enviar el valor de PWM máximo al ESP32
    send_pwm_to_esp32(max_speed)

    print("Controls updated.")

def update_info():
    odometry_label.config(text="Odometer: 120 cm")
    status_label.config(text="Status: Moving")
    station_label.config(text="Current Station: None")

# Crear la ventana principal
root = tk.Tk()
root.title("Autonomous Toy Train Control")

# Crear un contenedor de pestañas
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Pestaña de controles
control_tab = ttk.Frame(notebook)
notebook.add(control_tab, text="Train Controls")

# Elementos de la pestaña de controles
ttk.Label(control_tab, text="Set Maximum Speed (pwm):").grid(row=0, column=0, padx=10, pady=5)
max_speed_entry = ttk.Entry(control_tab)
max_speed_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(control_tab, text="Set Minimum Speed (pwm):").grid(row=1, column=0, padx=10, pady=5)
min_speed_entry = ttk.Entry(control_tab)
min_speed_entry.grid(row=1, column=1, padx=10, pady=5)

start_button = ttk.Button(control_tab, text="Start", command=start_train)
start_button.grid(row=2, column=0, padx=10, pady=5)

update_button = ttk.Button(control_tab, text="Update Info", command=update_controls)
update_button.grid(row=2, column=1, padx=10, pady=5)

stop_button = ttk.Button(control_tab, text="Emergency Stop", command=stop_train)
stop_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

ttk.Label(control_tab, text="Station Wait Time (s):").grid(row=4, column=0, padx=10, pady=5)
wait_time_entry = ttk.Entry(control_tab)
wait_time_entry.grid(row=4, column=1, padx=10, pady=5)

# Pestaña de información
info_tab = ttk.Frame(notebook)
notebook.add(info_tab, text="Train Information")

odometry_label = ttk.Label(info_tab, text="Odometer: ---")
odometry_label.grid(row=0, column=0, padx=10, pady=5)

status_label = ttk.Label(info_tab, text="Status: ---")
status_label.grid(row=1, column=0, padx=10, pady=5)

station_label = ttk.Label(info_tab, text="Current Station: ---")
station_label.grid(row=2, column=0, padx=10, pady=5)

update_odom_button = ttk.Button(info_tab, text="Update Odometry", command=update_info)
update_odom_button.grid(row=3, column=0, padx=10, pady=5)

# Ejecutar la interfaz
root.mainloop()
