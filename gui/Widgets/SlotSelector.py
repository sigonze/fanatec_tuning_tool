import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from typing import Callable


SLOT_TEXT = [
    "- no slot change -",
    "A SET",
    "SET 1",
    "SET 2",
    "SET 3",
    "SET 4",
    "SET 5",
]


class SlotSelector(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)

        self.callbacks = {
            "settings-updated": None
        }

        self.slot_selection = Gtk.DropDown.new_from_strings(SLOT_TEXT)
        self.slot_selection.connect("notify::selected-item", self.__on_slot_changed)

        left_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        right_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.append(left_box)
        self.append(self.slot_selection)
        self.append(right_box)
        left_box.set_hexpand(True)
        self.slot_selection.set_hexpand(True)
        right_box.set_hexpand(True)


    def get_value(self) -> int:
        return self.slot_selection.get_selected()


    def set_value(self,slot_value):
        if slot_value < 0 or slot_value > len(SLOT_TEXT)+1:
            self.slot_selection.set_selected(0)
        else:
            self.slot_selection.set_selected(slot_value)


    def connect(self, event_name, callback: Callable[[str], None]):
        assert event_name in self.callbacks.keys()
        self.callbacks[event_name]=callback


    def __on_slot_changed(self, slot_selection, param):
        selected_item = slot_selection.get_selected_item()
        if selected_item:
            value = self.get_value()
            if self.callbacks["settings-updated"]:
                self.callbacks["settings-updated"]({ "SLOT": value })
