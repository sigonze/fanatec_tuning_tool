import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from typing import Callable


class Slider(Gtk.Grid):
    def __init__(self, name: str, min=None, max=None, step=None, default=None, marks=None, description=None):
        super().__init__()

        self.callbacks = {
            "setting-updated": None
        }

        self.name = name

        # default values
        if min is None:
            min=0
        if max is None:
            max=100
        if step is None:
            step=1
        if default is None:
            default=max
        if marks is None:
            marks = {
                "OFF": min,
                f"{max}": max,
            }
        if not default in marks.values():
            marks[f"{default}"]=default
        if not min in marks.values():
            marks[f"{min}"]=min
        if not max in marks.values():
            marks[f"{max}"]=max

        self.min=min
        self.max=max
        self.step=step

        # Slider name
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        if len(description)>0:
            description_label=Gtk.Label(label=description)
            hbox.append(description_label)
            name_label=Gtk.Label(label=f"({name})")
        else:
            name_label=Gtk.Label(label=name)
        hbox.append(name_label)
        
        # Slider
        value=min
        adjustment = Gtk.Adjustment(value=value, lower=min, upper=max, step_increment=step)
        self.slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        self.slider.connect("value-changed", self.__on_slider_changed)

        for l, v in marks.items():
            self.slider.add_mark(v, Gtk.PositionType.TOP, l)
            self.slider.set_size_request(200, -1)

        # Slider value
        self.value_label = Gtk.Label(label=str(value))

        # Presentation
        hbox.set_size_request(200, -1)
        self.slider.set_hexpand(True)
        self.value_label.set_size_request(80, -1)
        
        self.attach(hbox, 0, 1, 1, 1) 
        self.attach(self.slider, 1, 1, 1, 1)
        self.attach(self.value_label, 2, 1, 1, 1) 


    def connect(self, event_name, callback: Callable[[str], None]):
        assert event_name in self.callbacks.keys()
        self.callbacks[event_name]=callback


    def get_value(self):
        return int(self.slider.get_value())


    def set_value(self, value: int):
        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max
        snapped_value=(value//self.step)*self.step 
        self.slider.set_value(snapped_value)
        self.value_label.set_text(str(snapped_value))


    def __on_slider_changed(self, slider):
        value=int(slider.get_value())
        snapped_value=(value//self.step)*self.step 
        self.slider.set_value(snapped_value)
        self.value_label.set_text(str(snapped_value))
        if self.callbacks["setting-updated"]:
            self.callbacks["setting-updated"]({ self.name: snapped_value })
