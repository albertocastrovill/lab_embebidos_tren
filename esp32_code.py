import network
import socket
from machine import Pin, PWM

# Define WiFi credentials
ssid = "Drone_Charging_Station"  # WiFi SSID
password = "dronedejoel"  # WiFi password

# Conectar a WiFi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
    pass

print("Connected to WiFi")
print("IP Address:", station.ifconfig()[0])

# Configuración del servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 80))  # Escuchar en el puerto 80
server_socket.listen(1)

print("Waiting for connections...")

# L293D motor control pins
motor_enable = PWM(Pin(23), freq=500)  # PWM pin
motor_in1 = Pin(18, Pin.OUT)  # GPIO pin
motor_in2 = Pin(19, Pin.OUT)  # GPIO pin

# Inicializa el motor
motor_in1.value(1)
motor_in2.value(0)
motor_enable.duty(0)

def set_motor_speed(speed):
    motor_enable.duty(max(0, min(speed, 1023)))
    print(f"Motor speed set to {speed}")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        data = client_socket.recv(1024).decode('utf-8')  # Recibir datos
        if data:
            print(f"Received: {data}")
            try:
                speed = int(data)
                set_motor_speed(speed)
            except ValueError:
                print("Invalid speed value received")
        client_socket.close()

except KeyboardInterrupt:
    print("Stopping server...")
    server_socket.close()
    motor_enable.duty(0)
