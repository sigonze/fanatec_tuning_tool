import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from typing import Callable


class ProfileList(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.callbacks = {
            "profile-added": None,
            "profile-removed": None,
            "profile-selected": None
        }

        self.profiles = {}
        self.selected_button = None

        # Create Profile List
        self.profile_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.append(self.profile_box)

        # Create an Entry for adding new profile
        self.new_profile_entry = Gtk.Entry()
        self.new_profile_entry.set_placeholder_text("Add new profile...")
        self.new_profile_entry.connect("activate", self.on_add_profile) 
        self.append(self.new_profile_entry)


    def create_profiles(self, profiles):
        for profile in profiles:
            self.add_profile(profile)


    def select_profile(self, profile_text):
        row = self.profiles.get(profile_text)
        if row:
            self.list_box.select_row(row)

    def get_selected_profile(self):
        if self.selected_button:
            return self.selected_button.get_label()
        return None

    def remove_profile(self, profile_text):
        index = len(self.profiles)
        if index > 1:
            row = self.profiles.get(profile_text)
            if row:
                self.list_box.remove(row)
                del self.profiles[profile_text]
                if self.callbacks["profile-removed"]:
                    self.callbacks["profile-removed"](profile_text)


    def add_profile(self, profile_text):
        # Create a horizontal box to hold the profile and the delete button
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        # Create a label for the profile
        profile_button = Gtk.ToggleButton(label=f"{profile_text}")
        profile_button.set_tooltip_text(f"load profile '{profile_text}'")
        profile_button.set_hexpand(True)
        profile_button.connect("toggled", self.on_profile_select)
        hbox.append(profile_button)

        # remove button
        delete_button = Gtk.Button(label="x")
        delete_button.connect("clicked", self.on_delete_button_clicked,profile_text)
        delete_button.set_tooltip_text(f"delete profile '{profile_text}'")
        hbox.append(delete_button)

        # Add to the profile list
        self.profile_box.append(hbox)
        self.profiles[profile_text]=hbox
        
        if self.callbacks["profile-added"]:
            self.callbacks["profile-added"](profile_text)
        
        return profile_button


    def connect(self, event_name, callback: Callable[[str], None]):
        assert event_name in self.callbacks.keys()
        self.callbacks[event_name]=callback


    def on_add_profile(self, new_profile):
        # Add profile to the ListBox
        new_profile_text = new_profile.get_text()
        if new_profile_text and not new_profile_text in self.profiles:
            button = self.add_profile(new_profile_text)
            button.set_active(True)
            self.new_profile_entry.set_text("")


    def on_delete_button_clicked(self, button, profile_text):
        # Remove the profile provided by the index
        if self.profiles.get(profile_text):
            self.profile_box.remove(self.profiles[profile_text])
            del self.profiles[profile_text]
            if self.callbacks["profile-removed"]:
                self.callbacks["profile-removed"](profile_text)

    def on_profile_select(self, button):
        if button.get_active():
            if button != self.selected_button:
                previous_selected = self.selected_button
                self.selected_button = button
                if previous_selected:
                    previous_selected.set_active(False)
                if self.callbacks["profile-selected"]:
                    self.callbacks["profile-selected"](button.get_label())
        elif button == self.selected_button:
            button.set_active(True)

