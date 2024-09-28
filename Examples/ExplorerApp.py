#!/usr/bin/env python3

import gi
import subprocess
import os

SYSFS_PATH="/sys/module/hid_fanatec/drivers/hid:fanatec/"

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Open Folder Example")
        self.set_default_size(300, 100)

        # button = Gtk.Button(label="L")
        # Create an image widget with a search icon
        # search_icon = Gtk.Image.new_from_icon_name("edit-find")
        search_icon = Gtk.Image.new_from_icon_name("folder")

        # Create a button and add the image to it
        button = Gtk.Button()
        button.set_child(search_icon)
        button.connect("clicked", self.on_button_clicked)

        self.set_child(button)

    def on_button_clicked(self, button):
        # Specify the folder you want to open
        # Check if the folder exists
        if os.path.isdir(SYSFS_PATH):
            # Open the file explorer
            subprocess.run(["xdg-open", SYSFS_PATH])
        else:
            print(f"Folder does not exist: {SYSFS_PATH}")


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