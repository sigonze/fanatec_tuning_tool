import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from typing import Callable


class ProfileList(Gtk.Box):
    def __init__(self, profiles):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.callbacks = {
            "profile-added": None,
            "profile-removed": None,
            "profile-selected": None
        }

        # Create Profile List
        self.profile_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.append(self.profile_box)

        # Create an Entry for adding new profile
        self.new_profile_entry = Gtk.Entry()
        self.new_profile_entry.set_placeholder_text("Add new profile...")
        self.new_profile_entry.connect("activate", self.__on_profile_added)
        self.append(self.new_profile_entry)

        # Add profiles
        self.profiles = {}
        for profile in profiles:
            self.__add_profile(profile)
        self.selected_profile = None


    def get_selected_profile(self):
        if self.selected_profile:
            return self.selected_profile.get_label()
        return None


    def __add_profile(self, profile_text):
        # Create a horizontal box to hold the profile and the delete button
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        # Create a label for the profile
        profile_button = Gtk.ToggleButton(label=f"{profile_text}")
        profile_button.set_tooltip_text(f"load profile '{profile_text}'")
        profile_button.set_hexpand(True)
        profile_button.connect("toggled", self.__on_profile_selected)
        hbox.append(profile_button)

        # remove button
        delete_button = Gtk.Button(label="x")
        delete_button.connect("clicked", self.__on_profile_removed,profile_text)
        delete_button.set_tooltip_text(f"delete profile '{profile_text}'")
        hbox.append(delete_button)

        # Add to the profile list
        self.profile_box.append(hbox)
        self.profiles[profile_text]=hbox

        return profile_button


    def __remove_profile(self, profile_text):
        index = len(self.profiles)
        if index > 1:
            row = self.profiles.get(profile_text)
            if row:
                self.list_box.remove(row)
                del self.profiles[profile_text]
                if self.callbacks["profile-removed"]:
                    self.callbacks["profile-removed"](profile_text)


    def connect(self, event_name, callback: Callable[[str], None]):
        assert event_name in self.callbacks.keys()
        self.callbacks[event_name]=callback


    def __on_profile_added(self, new_profile):
        # Add profile to the ListBox
        new_profile_text = new_profile.get_text()
        if new_profile_text and not new_profile_text in self.profiles:
            button = self.__add_profile(new_profile_text)
            button.set_active(True)
            self.new_profile_entry.set_text("")

            if self.callbacks["profile-added"]:
                self.callbacks["profile-added"](new_profile_text)


    def __on_profile_removed(self, button, profile_text):
        # Remove the profile provided by the index
        if self.profiles.get(profile_text):
            self.profile_box.remove(self.profiles[profile_text])
            del self.profiles[profile_text]

            if self.callbacks["profile-removed"]:
                self.callbacks["profile-removed"](profile_text)


    def __on_profile_selected(self, button):
        if button.get_active():
            if button != self.selected_profile:
                if self.selected_profile:
                    self.selected_profile.set_active(False)
                self.selected_profile = button

                if self.callbacks["profile-selected"]:
                    self.callbacks["profile-selected"](button.get_label())

        elif button == self.selected_profile:
            self.selected_profile = None
