#!/usr/bin/env python3

import configparser
import os
from io import StringIO
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .TuningPanel import TuningPanel
from .LateralPanel import LateralPanel

class MainWindow(Gtk.Window):
    def __init__(self, profile_file:str):
        super().__init__(title="Fanatec Tuning Tool")
        self.set_default_size(900, 500)
        self.profile_file=profile_file

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

        self.lateral_panel=LateralPanel()
        self.tuning_panel=TuningPanel()
        self.tuning_panel.set_hexpand(True)

        hbox.append(self.lateral_panel)
        hbox.append(self.tuning_panel)

        self.load_profile("default")

        self.set_child(hbox)


    def load_profile(self,profile: str):
        config = configparser.RawConfigParser(allow_no_value=True)
        config.optionxform = str
        config.read(self.profile_file)

        profile_values =[]
        for name, value in config.items(profile):
            profile_values.append((name, int(value)))
        self.tuning_panel.load_profile(profile_values)


class App(Gtk.Application):
    def __init__(self,profile_file:str):
        super().__init__()
        self.window = None
        self.profile_file = profile_file


    def do_activate(self):
        if not self.window:
            self.window = MainWindow(self.profile_file)
            self.window.set_application(self)
            self.window.connect("destroy", self.on_window_destroy)
        self.window.present()


    def on_window_destroy(self, widget):
        self.window = None