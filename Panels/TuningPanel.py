import gi
import os

from .Widgets import SlotSelector
from .Widgets import Slider

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

WORK_FOLDER = "Tests"
SLOT_FILE = "SLOT"
FILES = [ "SEN", "FF", "DRI", "FEI", "FOR", "SPR", "DPR", "BLI", "SHO" ]


class TuningPanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.set_margin_top(20)
        self.set_margin_bottom(20)
        self.set_margin_start(20)
        self.set_margin_end(20)

        slot_selector=SlotSelector(os.path.join(WORK_FOLDER,SLOT_FILE))
        self.append(slot_selector)

        for f in FILES:
            slider=Slider(file_name=os.path.join(WORK_FOLDER,f), shortname=f)
            self.append(slider)
