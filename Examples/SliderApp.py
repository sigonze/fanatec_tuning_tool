#!/usr/bin/env python3

import gi
import os

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

# Base name for slider value files
VALUE_FILE_BASE = 'slider_value_'

class SliderWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Slider Example")
        self.set_default_size(400, 200)  # Increased width for better layout

        # Load values from the files
        self.values = self.load_values()

        # Create a vertical box to hold sliders and labels
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.sliders = []
        self.labels = []  # List to hold labels for each slider

        # Create sliders based on loaded values
        for i, value in enumerate(self.values):
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)  # Horizontal box for slider and label

            slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 1)
            slider.set_value(value)
            slider.connect("value-changed", self.on_slider_changed, i)
            slider.set_hexpand(True)  # Allow the slider to expand horizontally

            label = Gtk.Label(label=str(value))  # Create a label to display the current value
            self.labels.append(label)  # Store the label for later updates

            hbox.append(slider)  # Add the slider to the horizontal box
            hbox.append(label)    # Add the label to the horizontal box

            vbox.append(hbox)  # Add the horizontal box to the vertical box
            self.sliders.append(slider)

        self.set_child(vbox)  # Use set_child instead of add

    def load_values(self):
        """Load values from individual files or return default values."""
        values = []
        for i in range(5):  # Change the number of sliders as needed
            file_name = f"{VALUE_FILE_BASE}{i}.txt"
            if os.path.exists(file_name):
                with open(file_name, 'r') as f:
                    values.append(int(f.read().strip()))
            else:
                values.append(0)  # Default value if the file does not exist
        return values

    def on_slider_changed(self, slider, index):
        """Update the file and label when a slider value changes."""
        self.values[index] = int(slider.get_value())
        self.labels[index].set_text(str(self.values[index]))  # Update the label with the new value
        self.save_value(index)  # Save the value to the corresponding file

    def save_value(self, index):
        """Save the current slider value to its corresponding file."""
        file_name = f"{VALUE_FILE_BASE}{index}.txt"
        with open(file_name, 'w') as f:
            f.write(str(self.values[index]))

class SliderApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyGtkApplication")
        self.window = None  # Keep a reference to the window

    def do_activate(self):
        if not self.window:  # Create the window only once
            self.window = SliderWindow()
            self.window.set_application(self)  # Set the application for the window
            self.window.connect("destroy", self.on_window_destroy)  # Connect the destroy signal

        self.window.present()  # Show the window

    def on_window_destroy(self, widget):
        self.window = None  # Clear the reference when the window is closed

def main():
    app = SliderApp()
    app.run(None)

if __name__ == "__main__":
    main()

