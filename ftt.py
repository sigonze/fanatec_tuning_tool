#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

from gui import App



def main():
    app = App(profile_dir="profiles")
    app.run(None)

if __name__ == "__main__":
    main()