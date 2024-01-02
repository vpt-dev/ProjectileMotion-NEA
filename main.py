# main.py

import tkinter as tk
from Authenticator import Authenticator
from SimulatorManager import SimulatorManager
import easygui
import numpy as np

def on_authentication_success():
    simulator_manager = SimulatorManager()
    simulator_manager.v = float(field_values[0])  # Initial velocity
    simulator_manager.theta = float(field_values[1]) * np.pi / 180.0  # Initial angle in radians
    simulator_manager.run_simulation()

# Tkinter main loop for login system
window = tk.Tk()
window.title("Login")
window.minsize(600, 300)  # Set minimum size

# Easy GUI for input
msg = "Enter velocity & angle"
title = "Input for projectile simulation"
field_names = ["Velocity", "Angle"]
field_values = []  # Initialize with blank values

# Display a dialog to input the values
field_values = easygui.multenterbox(msg, title, field_names)

# Ensure that the user provides values
while field_values is not None:
    errmsg = ""
    for i in range(len(field_names)):
        if field_values[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % field_names[i])
    if errmsg == "":
        break  # No empty fields
    field_values = easygui.multenterbox(errmsg, title, field_names, field_values)

# Check if the user canceled the input
if field_values is None:
    exit()

# Convert the input values to floats
simulator_manager = SimulatorManager()
simulator_manager.v = float(field_values[0])  # Initial velocity
simulator_manager.theta = float(field_values[1]) * np.pi / 180.0  # Initial angle in radians

# Authenticator
email_label = tk.Label(window, text="Email:")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()
password_entry = tk.Entry(window, show="*")
password_entry.pack()

password_requirement_label = tk.Label(window, text="", fg="red")
password_requirement_label.pack()

authenticator = Authenticator(
    window,
    email_entry,
    password_entry,
    password_requirement_label,
    on_authentication_success  # Pass the callback function directly
)

button_frame = tk.Frame(window)
button_frame.pack()

signup_button = tk.Button(button_frame, text="Signup", command=authenticator.signup)
signup_button.pack(side="left")
login_button = tk.Button(button_frame, text="Login", command=authenticator.login)
login_button.pack(side="left")

window.mainloop()
