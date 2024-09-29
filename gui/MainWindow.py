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
    def __init__(self, profile_dir:str):
        super().__init__(title="Fanatec Tuning Tool")
        self.set_default_size(900, 500)
        self.profile_dir=profile_dir

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

        self.load_profile("ac.ini")

        self.set_child(hbox)


    def load_profile(self,profile_name: str):
        config = configparser.RawConfigParser(allow_no_value=True)
        with open(os.path.join(self.profile_dir,profile_name), 'r') as file:
            content = '[PROFILE]\n' + file.read() 
            print(f"{content}")
            profile = []
            config.optionxform = str
            config.read_file(StringIO(content))
            for name, value in config.items('PROFILE'):
                profile.append((name, int(value)))
            print(f"{profile}")
            self.tuning_panel.load_profile(profile)

class App(Gtk.Application):
    def __init__(self,profile_dir:str):
        super().__init__()
        self.window = None
        self.profile_dir = profile_dir

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(self.profile_dir)
            self.window.set_application(self)
            self.window.connect("destroy", self.on_window_destroy)

        self.window.present()

    def on_window_destroy(self, widget):
        self.window = None