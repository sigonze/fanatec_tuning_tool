import os
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class Slider(Gtk.Grid):
    def __init__(self, file_name: str, name: str, min=None, max=None, step=None, default=None, marks=None, description=None):
        super().__init__()

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
                min: "OFF",
                max: f"{max}",
            }
        if not default in marks:
            marks[default]= f"{default}"
        if not min in marks:
            marks[min]= f"{min}"
        if not max in marks:
            marks[max]= f"{max}"

        self.file_name=file_name
        self.min=min
        self.max=max
        self.step=step

        # Slider name
        hbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        if len(description)>0:
            description_label=Gtk.Label(label=description)
            hbox.append(description_label)
            name_label=Gtk.Label(label=f"({name})")
            hbox.append(name_label)
        else:
            name_label=Gtk.Label(label=name)
            hbox.append(name_label)   
        name_label.set_size_request(250, -1)         
        # self.name.set_halign(Gtk.Align.START)

        # Slider
        value=self.get_value()
        adjustment = Gtk.Adjustment(value=value, lower=min, upper=max, step_increment=step)
        self.slider = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        self.slider.connect("value-changed", self.on_slider_changed)

        for v, l in marks.items():
            self.slider.add_mark(v, Gtk.PositionType.TOP, l)

        # Slider value
        self.value_label = Gtk.Label(label=str(value))

        # Presentation
        hbox.set_size_request(100, -1)
        self.slider.set_hexpand(True)
        self.value_label.set_size_request(80, -1)
        
        self.attach(hbox, 0, 1, 1, 1) 
        self.attach(self.slider, 1, 1, 1, 1)
        self.attach(self.value_label, 2, 1, 1, 1) 


    def get_value(self):
        value = 0
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                value = int(f.read().strip())
        return value
    
    def set_value(self, value: int):
        if value < self.min:
            value = self.min
        if value > self.max:
            value = self.max
        snapped_value=(value//self.step)*self.step 
        self.slider.set_value(snapped_value)
        self.value_label.set_text(str(snapped_value))


    def on_slider_changed(self, slider):
        value=int(slider.get_value())
        snapped_value=(value//self.step)*self.step 
        self.slider.set_value(snapped_value)
        self.value_label.set_text(str(snapped_value))
        with open(self.file_name, 'w') as f:
            f.write(str(snapped_value))
