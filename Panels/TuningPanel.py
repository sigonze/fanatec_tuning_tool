import gi
import os

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from .Widgets import SlotSelector
from .Widgets import Slider


WORK_FOLDER = "Tests"
SLOT_FILE = "SLOT"

FANATEC_FFB_SETTINGS = {
    "SEN": "Sensitivity",
    "FF" : "Force Feedback",
    "NDP": "Natural Damper",
    "NFR": "Natural Friction",
    "NIN": "Natural Inertia",
    "INT": "Force Feedback Interpolation",
    "FEI": "Force Effect Intensity",
    "FOR": "Force",
    "SPR": "Spring",
    "DPR": "Damper",
    "BLI": "Brake Level Indicator",
    "SHO": "Shock"
}


class TuningPanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.set_margin_top(5)
        self.set_margin_bottom(5)
        self.set_margin_start(5)
        self.set_margin_end(5)

        slot_selector=SlotSelector(os.path.join(WORK_FOLDER,SLOT_FILE))
        self.append(slot_selector)

        for effect, description in FANATEC_FFB_SETTINGS.items():
            slider=Slider(file_name=os.path.join(WORK_FOLDER,effect), name=effect, description=description)
            self.append(slider)
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            * {
                font-size: 10px;  /* Set the global font size */
            }
        """)

        # Apply the CSS to the entire application
        style_context = self.get_style_context()
        style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
