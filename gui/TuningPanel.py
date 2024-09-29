import gi
import os

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .Widgets import SlotSelector
from .Widgets import Slider


WORK_FOLDER = "Tests"
SLOT_FILE = "SLOT"

FANATEC_FFB_SETTINGS = {
    "SEN": { "description": "Sensitivity", 
             "min": 10, 
             "max": 2530,
             "default": 2530,
             "step": 10,
             "marks": { 360: "360", 1080: "1080", 2530: "AUTO" } },
    "FF" : { "description": "Force Feedback", "default": 100 },
    "NDP": { "description": "Natural Damper", "default": 50 },
    "NFR": { "description": "Natural Friction" },
    "NIN": { "description": "Natural Inertia", "max": 20, "default": 11 },
    "INT": { "description": "Force Feedback Interpolation" },
    "FEI": { "description": "Force Effect Intensity" },
    "FOR": { "description": "Force", "max": 120, "default": 100 },
    "SPR": { "description": "Spring", "max": 120, "default": 100 },
    "DPR": { "description": "Damper", "max": 120, "default": 100 },
    "BLI": { "description": "Brake Level Indicator", 
             "min": 1,
             "max": 101,
             "marks": { 101: "OFF" } },
    "SHO": { "description": "Shock" }
}


class TuningPanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        slot_selector=SlotSelector(os.path.join(WORK_FOLDER,SLOT_FILE))
        self.append(slot_selector)

        for key, settings in FANATEC_FFB_SETTINGS.items():
            description = settings.get("description")
            min = settings.get("min")
            max = settings.get("max")
            step = settings.get("step")
            default = settings.get("default")
            marks = settings.get("marks")
            slider=Slider(
                file_name=os.path.join(WORK_FOLDER,key), 
                name=key, 
                description=description,
                min=min,
                max=max,
                step=step,
                default=default,
                marks=marks
            )
            self.append(slider)