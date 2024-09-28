#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from Panels import TuningPanel

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Fanatec Tuning Tool")
        self.set_default_size(500, 400)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        tuning_panel=TuningPanel()
        vbox.append(tuning_panel)

        self.set_child(vbox)

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

