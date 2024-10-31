from tkinter import *
from tkinter import ttk
#import RPi.GPIO as GPIO

# Configuración del GPIO
LED_PIN = 18
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(LED_PIN, GPIO.OUT)
#GPIO.output(LED_PIN, GPIO.LOW)

# Crear ventana principal
root = Tk()
root.title("Control de LED con Tkinter y GPIO")
root.geometry("400x250")
root.configure(bg="#f0f0f0")
root.resizable(0, 0)

led = False

def encender():
    global led
    led = True
    #GPIO.output(LED_PIN, GPIO.HIGH)  # Encender LED físico
    label_status.config(text="Estado del LED: Encendido", foreground="green")

def apagar():
    global led
    led = False
    #GPIO.output(LED_PIN, GPIO.LOW)  # Apagar LED físico
    label_status.config(text="Estado del LED: Apagado", foreground="red")

# Estilo de los botones
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)

# Botones para encender y apagar el LED
boton_encender = ttk.Button(root, text="Encender LED", width=15 ,command=encender)
boton_encender.place(x=120, y=50)

boton_apagar = ttk.Button(root, text="Apagar LED", width=15 ,command=apagar)
boton_apagar.place(x=120, y=110)

# Etiqueta para mostrar el estado del LED
label_status = Label(root, text="Estado del LED: Apagado", font=("Arial", 14), bg="#f0f0f0", foreground="red")
label_status.place(x=100, y=180)

# Iniciar bucle de la interfaz
root.mainloop()

# Limpiar configuración de GPIO al salir
#GPIO.cleanup()


