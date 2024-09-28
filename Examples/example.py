#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

class MyApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id="com.example.MyApp")

    def do_activate(self):
        window = MyApplicationWindow(application=self)
        window.present()

class MyApplicationWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a navigation pane
        self.navigation_pane = Adw.NavigationView()

        # Create a stack for the main content
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)

        # Create some example pages
        self.create_pages()

        # Create a stack switcher for navigation
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(self.stack)

        # Set the stack and the stack switcher in the navigation pane
        #self.navigation_pane.set_stack(self.stack)
        self.navigation_pane.set_sidebar(stack_switcher)

        # Set the navigation pane as the content of the window
        self.set_content(self.navigation_pane)

    def create_pages(self):
        # Create example pages
        page1 = Gtk.Label(label="Page 1")
        page2 = Gtk.Label(label="Page 2")
        page3 = Gtk.Label(label="Page 3")

        # Add pages to the stack
        self.stack.add_child(page1)
        self.stack.add_child(page2)
        self.stack.add_child(page3)

if __name__ == "__main__":
    app = MyApplication()
    app.run()

