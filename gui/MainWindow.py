#!/usr/bin/env python3

import os
import json
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .TuningPanel import TuningPanel
from .LateralPanel import LateralPanel


script_dir = os.path.dirname(os.path.abspath(__file__))


class MainWindow(Gtk.Window):
    def __init__(self, profile_file:str):
        super().__init__(title="Fanatec Tuning Tool")
        self.set_default_size(900, 500)
        self.profile_file=profile_file

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.join(script_dir,"style.css"))

        # Apply the CSS to the entire application
        style_context = self.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)

        hbox.set_margin_top(20)
        hbox.set_margin_bottom(20)
        hbox.set_margin_start(20)
        hbox.set_margin_end(20)

        with open(self.profile_file, 'r') as json_file:
            self.profiles = json.load(json_file)

        self.lateral_panel=LateralPanel()
        self.lateral_panel.add_profiles(self.profiles.keys())
        self.tuning_panel=TuningPanel()
        self.tuning_panel.set_hexpand(True)

        hbox.append(self.lateral_panel)
        hbox.append(self.tuning_panel)

        self.load_profile("Default")

        self.set_child(hbox)


    def load_profile(self,profile: str):
        if profile not in self.profiles:
            raise ValueError(f"Profile '{profile}' not found in the JSON file.")

        self.tuning_panel.load_profile(self.profiles[profile])


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