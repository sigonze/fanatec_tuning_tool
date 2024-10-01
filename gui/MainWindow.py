#!/usr/bin/env python3

import os
import json
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .TuningPanel import TuningPanel
from .LateralPanel import LateralPanel


script_dir = os.path.dirname(os.path.abspath(__file__))


DEFAULT_VALUES = {
    "SEN": 2530,
    "FF": 100,
    "NDP": 50,
    "NFR": 0,
    "NIN": 0,
    "INT": 11,
    "FEI": 100,
    "FOR": 100,
    "SPR": 100,
    "DPR": 100,
    "BLI": 101,
    "SHO": 100
}



class MainWindow(Gtk.Window):
    def __init__(self, profile_file:str):
        super().__init__(title="Fanatec Tuning Tool")
        self.set_default_size(1000, 500)
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

        self.profiles = self.load_profiles()

        self.lateral_panel=LateralPanel(self.profiles.keys())
        self.lateral_panel.set_hexpand(False)
        self.lateral_panel.connect("profile-added", self.on_profile_added)
        self.lateral_panel.connect("profile-removed", self.on_profile_removed)
        self.lateral_panel.connect("profile-selected", self.on_profile_selected)

        self.tuning_panel=TuningPanel(DEFAULT_VALUES)
        self.tuning_panel.set_hexpand(True)

        hbox.append(self.lateral_panel)
        hbox.append(self.tuning_panel)

        self.set_child(hbox)


    def load_profiles(self):
        with open(self.profile_file, 'r') as json_file:
            return json.load(json_file)


    def save_profiles(self):
        with open(self.profile_file, 'w') as json_file:
            json.dump(self.profiles, json_file, indent=4)


    def on_profile_added(self, profile_name):
        self.profiles[profile_name] = {}
        self.save_profiles()


    def on_profile_removed(self, profile_name):
        if profile_name in self.profiles:
            del self.profiles[profile_name]
            self.save_profiles()


    def on_profile_selected(self, profile_name):
        if profile_name in self.profiles:
            self.tuning_panel.load_profile(self.profiles[profile_name])


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