import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class LateralPanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.profile_buttons = []

        info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        refresh_button = Gtk.Button()
        refresh_icon = Gtk.Image.new_from_icon_name("view-refresh")
        refresh_icon.set_pixel_size(10)
        refresh_button.set_child(refresh_icon)
        refresh_button.set_tooltip_text("Search hardware")

        load_icon = Gtk.Image.new_from_icon_name("go-up")
        load_button = Gtk.Button()
        load_button.set_child(load_icon)
        load_button.set_tooltip_text("Retrieve from hardware")

        self.wheel_label=Gtk.Label(label='Base: CSL DD\nWheel: McLaren GT3')
        self.wheel_label.set_hexpand(True)
        self.wheel_label.set_halign(Gtk.Align.START)

        info_box.append(refresh_button)
        info_box.append(self.wheel_label)
        info_box.append(load_button)

        spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        spacer.set_size_request(-1, 10)

        self.profile_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        self.add_profiles([])

        save_button = Gtk.Button(label="Save")
        apply_button = Gtk.Button(label="Apply")

        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        save_button.set_hexpand(True)
        apply_button.set_hexpand(True)
        action_box.append(save_button)
        action_box.append(apply_button)

        add_button = Gtk.Button()
        add_icon = Gtk.Image.new_from_icon_name("list-add")
        add_icon.set_pixel_size(10)
        add_button.set_child(add_icon)
        add_button.connect("clicked", self.on_profile_create)

        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter profile name")
        self.entry.set_visible(False)
        self.entry.connect("activate", self.on_entry)

        filler = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        filler.set_vexpand(True)

        self.append(info_box)
        self.append(spacer)
        self.append(self.profile_box)
        self.append(self.entry)
        self.append(add_button)
        self.append(filler)
        self.append(action_box)


    def create_profile_button(self,profile):
        button = Gtk.ToggleButton(label=f"{profile}")
        button.set_tooltip_text(f"load profile '{profile}'")
        button.set_hexpand(True)
        button.connect("toggled", self.on_profile_change)
        self.profile_buttons.append(button)

        remove_button = Gtk.Button()
        remove_icon = Gtk.Image.new_from_icon_name("edit-delete")
        remove_icon.set_pixel_size(10)
        remove_button.set_child(remove_icon)
        remove_button.set_tooltip_text(f"delete profile '{profile}'")
        remove_button.connect("clicked", self.on_profile_delete,profile)
        
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        button_box.set_name(profile)
        button_box.append(button)
        button_box.append(remove_button)
        return button_box


    def add_profiles(self, profiles):
        child = self.profile_box.get_first_child()
        while not child is None:
            self.profile_box.remove(child)
            child = self.profile_box.get_first_child()
        
        self.profile_buttons = []

        for profile in profiles:
            profile_button=self.create_profile_button(profile)
            self.profile_box.append(profile_button)


    def on_profile_change(self,button):
        if button.get_active():
            for b in self.profile_buttons:
                if b != button:
                    b.set_active(False)


    def on_profile_delete(self,button,profile):
        child = self.profile_box.get_first_child()
        while child is not None:
            print(child)
            if child.get_name() == profile:
                self.profile_box.remove(child)
                break
            child = child.get_next_sibling()

    def on_profile_create(self,button):
        self.entry.set_visible(True)
        self.entry.grab_focus()
    
    def on_entry(self,entry):
        print(entry)
        self.entry.set_visible(False)

    def on_entry_focus_out(self, entry):
        self.entry.grab_focus()