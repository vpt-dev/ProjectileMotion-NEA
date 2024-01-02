# SimulatorManager.py

import easygui
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Use a Tkinter backend
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns

class SimulatorManager:
    def __init__(self):
        self.v = None
        self.theta = None
        self.g = 9.81  # Default gravity value
        self.t = None
        self.r = None
        self.h = None
        self.x_projectile = None
        self.y_projectile = None
        self.coords_text = None
        self.t_values = None
        self.x_values = None
        self.y_values = None
        self.line = None

    def update_coordinates(self, i):
        if i < len(self.t_values):
            x_projectile = self.v * np.cos(self.theta) * (self.t_values[i])
            y_projectile = (self.v * np.sin(self.theta) * (self.t_values[i])) - (0.5) * self.g * (self.t_values[i]) ** 2
            self.coords_text.set_text(f'X: {x_projectile:.2f}, Y: {y_projectile:.2f}')
            self.line.set_data(self.x_values[:i], self.y_values[:i])
        else:
            self.coords_text.set_text("Projectile off screen")
        return self.coords_text, self.line

    def run_simulation(self):
        sns.set()
        fig, ax = plt.subplots()
        self.t = 2 * self.v * np.sin(self.theta) / self.g
        r_for_h = self.v * np.cos(self.theta) * (self.t / 2)
        self.h = ((self.v ** 2) * (np.sin(self.theta) ** 2)) / (2 * self.g)
        self.r = (self.v ** 2) * np.sin(2 * self.theta) / self.g
        time_text = "Flight Time: " + str(round(self.t, 2)) + 's'
        h_point = "Highest Point: " + str(round(self.h, 2)) + 'm'
        range_projectile = "Range: " + str(round(self.r, 2)) + 'm'

        self.x_projectile = 0
        self.y_projectile = 0

        self.coords_text = ax.text(0.1, 0.9, f'X: {self.x_projectile:.2f}, Y: {self.y_projectile:.2f}', transform=ax.transAxes)

        self.t_values = np.arange(0, self.t, 0.01)
        self.x_values = self.v * np.cos(self.theta) * self.t_values
        self.y_values = (self.v * np.sin(self.theta) * self.t_values) - (0.5) * self.g * (self.t_values) ** 2

        self.line, = ax.plot(self.x_values, self.y_values)
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.xlabel('Distance (x)')
        plt.ylabel('Distance (y)')
        plt.axis([-1.0, self.r + 5, 0, max(self.y_values) + 2])
        ax.set_autoscale_on(False)

        ani = animation.FuncAnimation(fig, self.update_coordinates, frames=len(self.t_values) + 50, interval=20)

        # Display the animation without saving it
        plt.show(block=True)


if __name__ == "__main__":
    simulator_manager = SimulatorManager()

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
    simulator_manager.v = float(field_values[0])  # Initial velocity
    simulator_manager.theta = float(field_values[1]) * np.pi / 180.0  # Initial angle in radians

    # Run simulation
    simulator_manager.run_simulation()
