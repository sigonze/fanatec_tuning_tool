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
        # Create a ListBox to hold the items
        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.append(self.list_box)

        self.profiles = {}

        # Create an Entry for adding new prfoile
        self.new_profile_entry = Gtk.Entry()
        self.new_profile_entry.set_placeholder_text("Add new profile...")
        self.new_profile_entry.connect("activate", self.on_add_profile) 

        # Add the Entry to the ListBox
        self.list_box.append(self.new_profile_entry)


    def create_profiles(self, profiles):
        for profile in profiles:
            self.add_profile(profile)


    def select_profile(self, profile_text):
        row = self.profiles.get(profile_text)
        if row:
            self.list_box.select_row(row)


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
        label = Gtk.Button(label=profile_text)
        label.connect("clicked", self.on_select_profile)
        label.set_hexpand(True)
        hbox.append(label)

        # Create a delete button
        delete_button = Gtk.Button(label="x")
        delete_button.connect("clicked", self.on_delete_button_clicked,profile_text)
        hbox.append(delete_button)

        # Add the box to the list and select it
        index = len(self.profiles)
        row = Gtk.ListBoxRow()
        row.set_child(hbox)
        self.list_box.insert(row, index)
        self.profiles[profile_text] = row
        self.select_profile(profile_text)

        if self.callbacks["profile-added"]:
            self.callbacks["profile-added"](profile_text)


    def connect(self, event_name, callback: Callable[[str], None]):
        assert event_name in self.callbacks.keys()
        self.callbacks[event_name]=callback


    def on_add_profile(self, new_profile):
        # Add profile to the ListBox
        new_profile_text = new_profile.get_text()
        if new_profile_text and not new_profile_text in self.profiles:
            self.add_profile(new_profile_text)
            self.new_profile_entry.set_text("")

    def on_delete_button_clicked(self, button, profile_text):
        # Remove the profile provided by the index
        self.remove_profile(profile_text)

    def on_select_profile(self, button):
        profile_text=button.get_label()
        self.select_profile(profile_text)
        if self.callbacks["profile-selected"]:
            self.callbacks["profile-selected"](profile_text)
