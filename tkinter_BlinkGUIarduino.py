import serial
from tkinter import *
import tkinter as tk
from tkinter import messagebox, ttk
import time

commPort = '/dev/cu.usbserial-1110'

# Connecting serial port and error tracing
try:
    ser = serial.Serial(commPort, baudrate=9600, timeout=1)
except serial.SerialException:
    messagebox.showerror("Connection Error", "Unable to connect to the device.")
    exit()

def turnOnLED():
    if blinkState.get() == 1:
        blinkLED()
    else:
        ser.write(b'o')
        updateStatus("ON")

def turnOffLED():
    ser.write(b'x')
    updateStatus("OFF")

def blinkLED():
    if blinkState.get() == 1:
        ser.write(b'b')
        time.sleep(1)
        delay = str(blinkSpeed.get())  # Blink duration from slider
        numBlinks = comboBlink.get()  # Number of blinks received from Combobox
        if userDataCheck(numBlinks):
            dataToSend = delay + '-' + numBlinks
            ser.write(dataToSend.encode())

def userDataCheck(userInput):
    try:
        value = int(userInput)
        if value < 1:
            raise ValueError("Blink count must be positive.")
        return True
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {e}", icon='error')
        return False

def menuBlinkEnable():
    if blinkState.get() != 1:
        blinkState.set(1)
    blinkLED()

def menuTurnOn():
    if blinkState.get() == 1:
        blinkState.set(0)
    ser.write(b'o')
    updateStatus("ON")

def menuTurnOff():
    if blinkState.get() == 1:
        blinkState.set(0)
    ser.write(b'x')
    updateStatus("OFF")

def menuSave():
    print("Selected Save")

def exitGUI():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

def updateStatus(status):
    ledStatus.config(text=f"LED Status: {status}", fg="green" if status == "ON" else "red")

def createTooltip(widget, text):
    tooltip = tk.Label(root, text=text, bg="yellow", relief="solid", bd=1, padx=5, pady=2)
    tooltip.place_forget()

    def show(event):
        tooltip.place(x=event.x_root - root.winfo_x(), y=event.y_root - root.winfo_y())

    def hide(event):
        tooltip.place_forget()

    widget.bind("<Enter>", show)
    widget.bind("<Leave>", hide)

# Tkinter Window Settings
root = Tk()
root.title('Blink GUI with Tkinter')
root.configure(bg='#f0f0f0')
root.geometry("400x400")

# LED Durum Etiketi
ledStatus = tk.Label(root, text="LED Status: OFF", fg="red", font=("Arial", 12))
ledStatus.grid(row=3, columnspan=3, pady=10)

# Turn On Button
btn_On = tk.Button(root, text="Turn On", command=turnOnLED)
btn_On.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
createTooltip(btn_On, "Turns the LED on")

# Turn Off Button
btn_Off = tk.Button(root, text="Turn Off", command=turnOffLED)
btn_Off.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
createTooltip(btn_Off, "Turns the LED off")

# Blink Checkbox
blinkState = IntVar()
chkBtn_Blink = tk.Checkbutton(root, text="Blink", variable=blinkState, command=blinkLED)
chkBtn_Blink.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
createTooltip(chkBtn_Blink, "Enables blinking mode")

# Slider for Blink Speed
blinkSpeed = Scale(root, from_=50, to=1200, orient=HORIZONTAL, label="Blink Speed (ms)", length=200)
blinkSpeed.set(800)  # Varsayılan değer
blinkSpeed.grid(row=1, columnspan=3, padx=10, pady=10)

# Combobox for Number of Blinks
numBlinksOptions = [str(i) for i in range(1, 21)]  # 1-20 arasında seçenekler
comboBlink = ttk.Combobox(root, values=numBlinksOptions, state='readonly', width=5)
comboBlink.set("5")  # Varsayılan değer
comboBlinkLabel = tk.Label(root, text="Num Blinks")
comboBlinkLabel.grid(row=2, column=0, padx=10, pady=10)
comboBlink.grid(row=2, column=1, padx=10, pady=10)

# Menu Bar
menuBar = Menu(root)

fileMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='File', menu=fileMenu)
fileMenu.add_command(label='Save', command=menuSave)
fileMenu.add_command(label='Exit', command=exitGUI)

settings = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label='Settings', menu=settings)
settings.add_command(label='Blink', command=menuBlinkEnable)
settings.add_command(label='Turn On', command=menuTurnOn)
settings.add_command(label='Turn Off', command=menuTurnOff)

root.config(menu=menuBar)

# Status Bar
statusBar = tk.Label(root, text="Status: Connected", bd=1, relief=SUNKEN, anchor=W)
statusBar.grid(row=4, columnspan=3, sticky='we')

# Main Loop
root.mainloop()
