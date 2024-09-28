import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class Slider(Gtk.Box):
    def __init__(self, file_name: str, min=0, max=100, step=1, marks={}, name="", shortname=""):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)

        self.file_name=file_name
        self.min=min
        self.max=max
        self.step=step

        if len(name)>0:
            self.name=Gtk.Label(label=str(name))
            self.name.set_halign(Gtk.Align.START)
            self.append(self.name)

        if len(marks)==0:
            marks = {
                min: "MIN",
                max: f"{max}",
            }


        hbox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        self.shortname = Gtk.Label(label=shortname)
        hbox.append(self.shortname)

        value=self.get_value()
        adjustment = Gtk.Adjustment(value=value, lower=min, upper=max, step_increment=step)

        self.slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        self.slider.connect("value-changed", self.on_slider_changed)
        self.slider.set_hexpand(True)

        for v, l in marks.items():
            self.slider.add_mark(v, Gtk.PositionType.BOTTOM, l)

        hbox.append(self.slider)

        self.label = Gtk.Label(label=str(value))
        hbox.append(self.label)
        self.append(hbox)


    def get_value(self):
        value = 0
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                value = int(f.read().strip())
        return value


    def on_slider_changed(self, slider):
        value=int(slider.get_value())
        snapped_value=(value//self.step)*self.step 
        self.slider.set_value(snapped_value)
        self.label.set_text(str(snapped_value))
        with open(self.file_name, 'w') as f:
            f.write(str(snapped_value))
