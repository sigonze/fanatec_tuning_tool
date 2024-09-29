import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class LateralPanel(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        self.base_label=Gtk.Label(label='Base: CSL DD')
        self.wheel_label=Gtk.Label(label='Wheel: McLaren GT3')
        spacer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        spacer.set_size_request(-1, 10)

        profile_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        for i in range(1, 5):
            button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            button = Gtk.Button(label=f"Button#{i}")
            # button.set_hexpand(True)
            button_box.append(button)
            remove_button = Gtk.Button(label="-")
            button_box.append(remove_button)
            profile_box.append(button_box)
        
        add_button = Gtk.Button(label="+")
        profile_box.append(add_button)

        load_button = Gtk.Button(label="Load")
        save_button = Gtk.Button(label="Save")
        apply_button = Gtk.Button(label="Apply")

        action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        action_box.append(load_button)
        action_box.append(save_button)
        action_box.append(apply_button)

        self.append(self.base_label)
        self.append(self.wheel_label)
        self.append(spacer)
        self.append(profile_box)

        profile_box.set_vexpand(True)
        self.append(action_box)