import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from typing import Callable

from .Widgets import ProfileList


class LateralPanel(Gtk.Box):
    def __init__(self,profiles):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # keep reference to wheel label to change it
        self.info_label=Gtk.Label()
        self.info_label.set_hexpand(True)
        self.info_label.set_halign(Gtk.Align.START)

        spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        spacer.set_size_request(-1, 10)

        # Create profile list
        self.profile_list = ProfileList(profiles)

        # Filler
        filler = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        filler.set_vexpand(True)

        # Create the panel
        self.append(self.profile_list)
        self.append(filler)
        self.append(spacer)
        self.append(self.info_label)


    def connect(self, event_name, callback: Callable[[str], None]):
        if event_name.startswith("profile-"):
            self.profile_list.connect(event_name,callback)


    def get_selected_profile(self):
        return self.profile_list.get_selected_profile()


    def update_info(self, info):
        info_text = "\n".join(f"{key}: {value}" for key, value in info.items()) 
        self.info_label.set_label(info_text)
