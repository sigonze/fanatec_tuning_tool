#!/usr/bin/env python3

import os
import json
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .TuningPanel import TuningPanel
from .LateralPanel import LateralPanel


script_dir = os.path.dirname(os.path.abspath(__file__))


DEFAULT_SETTINGS = {
    "SLOT": -1,
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

# DEFAULT_INFO = {
#     "Base": "CSL DD",
#     "Wheel": "McLaren GT3 V2"
# }
DEFAULT_INFO = {
    "MODE": "*** DEMO ***"
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

        self.profiles = self.__load_profiles()

        self.lateral_panel=LateralPanel(self.profiles.keys())
        self.lateral_panel.set_hexpand(False)
        self.lateral_panel.connect("profile-added", self.__on_profile_added)
        self.lateral_panel.connect("profile-removed", self.__on_profile_removed)
        self.lateral_panel.connect("profile-selected", self.__on_profile_selected)
        self.lateral_panel.update_info(DEFAULT_INFO)

        self.settings = DEFAULT_SETTINGS
        self.tuning_panel=TuningPanel(self.settings)
        self.tuning_panel.set_hexpand(True)
        self.tuning_panel.connect("setting-updated", self.__on_profile_updated)

        hbox.append(self.lateral_panel)
        hbox.append(self.tuning_panel)

        self.set_child(hbox)


    def __load_profiles(self):
        with open(self.profile_file, 'r') as json_file:
            return json.load(json_file)


    def __save_profiles(self):
        with open(self.profile_file, 'w') as json_file:
            json.dump(self.profiles, json_file, indent=4)


    def __on_profile_added(self, profile_name):
        self.settings = self.tuning_panel.get_settings()
        self.profiles[profile_name] = self.settings
        self.__save_profiles()


    def __on_profile_removed(self, profile_name):
        if profile_name in self.profiles:
            del self.profiles[profile_name]
            self.__save_profiles()


    def __on_profile_selected(self, profile_name):
        if profile_name in self.profiles:
            self.settings.update(self.profiles[profile_name])
            self.tuning_panel.update_settings(self.settings)


    def __on_profile_updated(self, setting_update):
        self.settings.update(setting_update)

        profile_name = self.lateral_panel.get_selected_profile()
        if profile_name:
            self.profiles[profile_name].update(setting_update)
            self.__save_profiles()

    def on_device_connected(self, device_info):
        self.lateral_panel.update_info(device_info)

    def on_device_disconnected(self, device_info):
        self.lateral_panel.update_info(device_info)
