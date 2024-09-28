#!/usr/bin/env python3

import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

# File to read from and write to
FILE_PATH = 'data.txt'

# Mapping of values to display text
SLOT_TEXT = [
    "A SET",
    "SET 1",
    "SET 2",
    "SET 3",
    "SET 4",
    "SET 5"
]


def read_value_from_file() -> int:
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def write_value_to_file(value: int):
    with open(FILE_PATH, 'w') as file:
        file.write(str(value))


class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Dropdown Example")

        # Load the current value from the file
        current_slot = read_value_from_file()
        
        # Create a ComboBox
        self.slot_selection = Gtk.DropDown.new_from_strings(SLOT_TEXT)
        self.slot_selection.set_selected(current_slot)
        self.slot_selection.connect("notify::selected-item", self.on_slot_changed)
        
        # Add the ComboBox to the window
        self.set_child(self.slot_selection)

    def on_slot_changed(self, slot_selection, param):
        """Handle the change in selection."""
        selected_item = slot_selection.get_selected_item()
        if selected_item:
            # Get the string value of the selected item
            active_value = selected_item.get_string()
            
            # Get the index of the selected item
            index = SLOT_TEXT.index(active_value)
            
            # Write the selected index to the file
            write_value_to_file(index)



            

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyGtkApplication")
        self.window = None  # Keep a reference to the window

    def do_activate(self):
        if not self.window:  # Create the window only once
            self.window = MainWindow()
            self.window.set_application(self)  # Set the application for the window
            self.window.connect("destroy", self.on_window_destroy)  # Connect the destroy signal

        self.window.present()  # Show the window

    def on_window_destroy(self, widget):
        self.window = None  # Clear the reference when the window is closed



def main():
    app = App()
    app.run(None)

if __name__ == "__main__":
    main()


