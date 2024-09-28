import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


SLOT_VALUES = [
    "A SET",
    "SET 1",
    "SET 2",
    "SET 3",
    "SET 4",
    "SET 5"
]


class SlotSelector(Gtk.Box):
    def __init__(self, file_name: str):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        self.file_name = file_name

        self.slot_selection = Gtk.DropDown.new_from_strings(SLOT_VALUES)
        self.slot_selection.set_selected(self.get_value())
        self.slot_selection.connect("notify::selected-item", self.on_slot_changed)

        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        self.append(left_box)
        self.append(self.slot_selection)
        self.append(right_box)
        left_box.set_hexpand(True)
        self.slot_selection.set_hexpand(True)
        right_box.set_hexpand(True)


    def get_value(self) -> int:
        value = 0
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                value = int(f.read().strip())
        return value

    def on_slot_changed(self, slot_selection, param):
        selected_item = slot_selection.get_selected_item()
        if selected_item:
            active_value = selected_item.get_string()
            index = SLOT_VALUES.index(active_value)
            with open(self.file_name, 'w') as file:
                file.write(str(index))
