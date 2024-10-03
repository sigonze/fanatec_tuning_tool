import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import os
import json
from typing import Callable


from .Widgets import SlotSelector
from .Widgets import Slider


script_dir = os.path.dirname(os.path.abspath(__file__))


class TuningPanel(Gtk.Box):
    def __init__(self, default_values):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        json_file_path = os.path.join(script_dir, 'fanatec_ffb_tuning.json')
        with open(json_file_path, 'r') as json_file:
            self.fanatec_ffb_settings = json.load(json_file)

        self.slot_selector=SlotSelector()
        self.append(self.slot_selector)
        self.sliders = {}
        self.update_settings(default_values)


    def add_slider(self, name: str):
        settings=self.fanatec_ffb_settings.get(name)
        if settings:
            if self.sliders.get(name) is None:
                description = settings.get("description")
                min = settings.get("min")
                max = settings.get("max")
                step = settings.get("step")
                default = settings.get("default")
                marks = settings.get("marks")
                slider=Slider(
                    name=name,
                    description=description,
                    min=min,
                    max=max,
                    step=step,
                    default=default,
                    marks=marks
                )
                self.sliders[name]=slider
                self.append(slider)


    def update_settings(self,settings: str):
        for key in self.sliders:
            if not key in settings.keys():
                self.remove(self.sliders[key])
                self.sliders[key]=None
        for key in settings:
            value = settings[key]
            if key == "SLOT":
                self.slot_selector.set_value(value)
            else:
                self.add_slider(key)
                if self.sliders.get(key):
                    self.sliders[key].set_value(value)

    def get_settings(self):
        settings = {}
        settings["SLOT"] = self.slot_selector.get_value()
        for setting, slider in self.sliders.items():
            settings[setting] = slider.get_value()
        return settings

    def connect(self, event_name, callback: Callable[[str], None]):
        self.slot_selector.connect(event_name, callback)
        for slider in self.sliders.values():
            slider.connect(event_name, callback)