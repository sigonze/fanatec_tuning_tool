import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class LateralPanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # keep references to button to add/remove them easily
        self.profile_buttons = {}
        self.toggle_buttons = []

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

        # empty profiles
        self.profile_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # action box
        save_button = Gtk.Button(label="Save")
        apply_button = Gtk.Button(label="Apply")

        action_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        save_button.set_hexpand(True)
        apply_button.set_hexpand(True)
        action_box.append(save_button)
        action_box.append(apply_button)

        add_button = Gtk.Button()
        add_icon = Gtk.Image.new_from_icon_name("list-add")
        add_button.set_child(add_icon)
        add_button.connect("clicked", self.on_profile_add)

        # create hidden entry for profile adding
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter profile name")
        self.entry.set_visible(False)
        self.entry.connect("activate", self.on_profile_create)

        filler = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        filler.set_vexpand(True)

        # create the panel
        self.append(info_box)
        self.append(spacer)
        self.append(self.profile_box)
        self.append(self.entry)
        self.append(add_button)
        self.append(filler)
        self.append(action_box)


    # create a profile button and associated remove button
    def create_profile_button(self,profile):
        # profile button
        button = Gtk.ToggleButton(label=f"{profile}")
        button.set_tooltip_text(f"load profile '{profile}'")
        button.set_hexpand(True)
        button.connect("toggled", self.on_profile_change)
        self.toggle_buttons.append(button)

        # remove button
        remove_button = Gtk.Button()
        remove_icon = Gtk.Image.new_from_icon_name("edit-delete")
        remove_icon.set_pixel_size(10)
        remove_button.set_child(remove_icon)
        remove_button.set_tooltip_text(f"delete profile '{profile}'")
        remove_button.connect("clicked", self.on_profile_delete,profile)

        # create the container to keep both
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        button_box.set_name(profile)
        button_box.append(button)
        button_box.append(remove_button)
        self.profile_buttons[profile]=button_box
        return button_box

    # add profiles
    def add_profiles(self, profiles):
        for profile in profiles:
            profile_button=self.create_profile_button(profile)
            self.profile_box.append(profile_button)


    # when a new profile is activated deactivate others
    def on_profile_change(self,button):
        if button.get_active():
            for b in self.toggle_buttons:
                if b != button:
                    b.set_active(False)


    # profile deletion
    def on_profile_delete(self,button,profile):
        if not self.profile_buttons.get(profile) is None:
            self.profile_box.remove(self.profile_buttons[profile])
            del self.profile_buttons[profile]


    # click on add button -> hidden entry appears
    def on_profile_add(self,button):
        self.entry.set_visible(True)
        self.entry.grab_focus()

    # create the profile
    def on_profile_create(self,entry):
        # if empty is empty -> cancel
        if len(self.entry.get_text()) == 0:
            self.entry.set_visible(False)
        # if entry already exists -> wait for a valid entry
        elif not self.entry.get_text() in self.profile_buttons:
            profile_button=self.create_profile_button(self.entry.get_text())
            self.profile_box.append(profile_button)
            self.entry.set_text("")
            self.entry.set_visible(False)
            self.toggle_buttons[-1].set_active(True)