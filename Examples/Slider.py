import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

class Slider(Gtk.Box):
    def __init__(self, min_value=0, max_value=100, step=10, initial_value=50):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        

        # Create a scale (slider) with a range based on the step size
        #self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, min_value // step, max_value // step, 1)
        #self.scale.set_value(initial_value // step)  # Set initial value
        #self.scale.connect("value-changed", self.on_scale_value_changed)
        
        self.step=step
        
        self.scale=Gtk.Scale()
        self.scale.set_range(min_value, max_value)
        self.scale.set_increments(step,0)
        self.scale.set_draw_value(True)
        self.scale.set_round_digits(0)
        self.scale.set_digits(0)
        self.scale.set_value(initial_value)
        self.scale.connect("value-changed", self.on_scale_value_changed)

        # Allow the slider to expand and fill the available space
        self.scale.set_hexpand(True)  # Allow horizontal expansion
        self.scale.set_vexpand(False)  # Do not allow vertical expansion

        # Set the scale to draw value and have origin
        self.scale.set_draw_value(True)  # Show the current value
        #self.scale.set_has_origin(False)  # Do not show origin marker

        # Create a label to display the current value
        self.label = Gtk.Label(label=f"Current Value: {initial_value:3}")
        self.label.set_halign(Gtk.Align.START)  # Align label to the start (left)

        # Add the slider and label to the main box
        self.append(self.scale)
        self.append(self.label)

        # Add marks to the scale
        #for i in range(min_value, max_value, step):
        #    self.scale.add_mark(i, Gtk.PositionType.BOTTOM, f"{i}")
        self.scale.add_mark(min_value, Gtk.PositionType.BOTTOM, "MIN")
        self.scale.add_mark(initial_value, Gtk.PositionType.BOTTOM, f"{initial_value}")
        self.scale.add_mark(max_value, Gtk.PositionType.BOTTOM, "MAX")
        
        # Load custom CSS
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")  # Load from the CSS file
        
        # Use add_provider_for_display for GTK 4
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def on_scale_value_changed(self, scale):
        # Get the current value and round it to the nearest integer
        value = int(scale.get_value())
        # Calculate the snapped value based on the step size
        snapped_value = (value // self.step) * self.step  # Assuming step size is 10
        self.scale.set_value(snapped_value)
        # Update the label with the current value
        self.label.set_text(f"Current Value: {snapped_value:3}")

    def get_value(self):
        # Return the current value of the slider
        return int(self.scale.get_value()) * 10



