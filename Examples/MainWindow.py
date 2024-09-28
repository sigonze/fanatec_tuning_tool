import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk, Adw

from Slider import Slider

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kargs):
        super().__init__(**kargs, title='Fanatec Configuration')

        navigation = Adw.NavigationSplitView()
        navigation.set_max_sidebar_width(178)
        navigation.set_min_sidebar_width(178)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        left = Adw.ToolbarView()
        left.add_top_bar(Adw.HeaderBar())
        left.set_content(vbox)

        sidebar = Adw.NavigationPage()
        sidebar.set_title('Fanatec Configuration')
        sidebar.set_child(left)

        navigation.set_sidebar(sidebar)
        navigation.set_content(Adw.NavigationPage(title="whatever"))

        #self.set_content(navigation)

        # Create a vertical box to hold the button and the slider
        #vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
       
        # Create an instance of StepSlider
        self.slider = Slider(min_value=0, max_value=100, step=10, initial_value=50)
        vbox.append(self.slider)

        self.slider2 = Slider(min_value=1, max_value=2530, step=10, initial_value=1080)
        vbox.append(self.slider2)

        # Create a button
        self.button = Gtk.Button(label='Apply')
        self.button.connect('clicked', self.on_button_clicked)
        
        # Add the button to the vertical box
        vbox.append(self.button)


        # Set the vertical box as the child of the window
        self.set_content(navigation)

    def on_button_clicked(self, _widget):
        print('Hello World')
        self.close()

