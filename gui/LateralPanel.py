import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from typing import Callable

from .Widgets import ProfileList

class LateralPanel(Gtk.Box):
    def __init__(self,profiles):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # create info box
        info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        refresh_button = Gtk.Button()
        refresh_icon = Gtk.Image.new_from_icon_name("view-refresh")
        refresh_button.set_child(refresh_icon)
        refresh_button.set_tooltip_text("Search hardware")

        load_icon = Gtk.Image.new_from_icon_name("go-next")
        load_button = Gtk.Button()
        load_button.set_child(load_icon)
        load_button.set_tooltip_text("Retrieve from hardware")

        # keep reference to wheel label to change it
        self.wheel_label=Gtk.Label(label='Base: CSL DD\nWheel: McLaren GT3')
        self.wheel_label.set_hexpand(True)
        self.wheel_label.set_halign(Gtk.Align.START)

        info_box.append(refresh_button)
        info_box.append(self.wheel_label)
        info_box.append(load_button)

        spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        spacer.set_size_request(-1, 10)

        # Add profiles
        self.profile_list = ProfileList()
        self.profile_list.create_profiles(profiles)

        # Filler
        filler = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        filler.set_vexpand(True)

        # Create the panel
        self.append(info_box)
        self.append(spacer)
        self.append(self.profile_list)
        self.append(filler)

    
    def connect(self, event_name, callback: Callable[[str], None]):
        if event_name.startswith("profile-"):
            self.profile_list.connect(event_name,callback)
    
    def get_selected_profile(self):
        return self.profile_list.get_selected_profile()