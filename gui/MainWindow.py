#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .TuningPanel import TuningPanel
from .LateralPanel import LateralPanel

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Fanatec Tuning Tool")
        self.set_default_size(800, 500)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            * {
                font-size: 14px;  /* Set the global font size */
            }
        """)

        # Apply the CSS to the entire application
        style_context = self.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=20)

        hbox.set_margin_top(20)
        hbox.set_margin_bottom(20)
        hbox.set_margin_start(20)
        hbox.set_margin_end(20)

        lateral_panel=LateralPanel()
        tuning_panel=TuningPanel()
        tuning_panel.set_hexpand(True)

        hbox.append(lateral_panel)
        hbox.append(tuning_panel)

        self.set_child(hbox)

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyGtkApplication")
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = MainWindow()
            self.window.set_application(self)
            self.window.connect("destroy", self.on_window_destroy)

        self.window.present()

    def on_window_destroy(self, widget):
        self.window = None