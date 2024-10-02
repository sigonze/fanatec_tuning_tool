import os
import json

import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .Widgets import SlotSelector
from .Widgets import Slider


WORK_FOLDER = "tests"
SLOT_FILE = "SLOT"


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
        self.load_profile(default_values)


    def add_slider(self, name: str):
        settings=self.fanatec_ffb_settings.get(name)
        if not settings is None:
            if self.sliders.get(name) is None:
                description = settings.get("description")
                min = settings.get("min")
                max = settings.get("max")
                step = settings.get("step")
                default = settings.get("default")
                marks = settings.get("marks")
                slider=Slider(
                    file_name=os.path.join(WORK_FOLDER,name), 
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


    def load_profile(self,profile: str):
        for key in self.sliders:
            if not key in profile.keys():
                self.remove(self.sliders[key])
                self.sliders[key]=None
        for key in profile:
            self.add_slider(key)
            if not self.sliders.get(key) is None:
                self.sliders[key].set_value(profile[key])



