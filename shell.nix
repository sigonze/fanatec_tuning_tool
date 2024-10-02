{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
#    pkgs.python3Packages.evdev
    pkgs.python3Packages.pyudev
    pkgs.python3Packages.pygobject3
    pkgs.gtk4
    pkgs.libadwaita
    pkgs.pkg-config
  ];

  shellHook = ''
    export PYTHONPATH=$PYTHONPATH:${pkgs.python3Packages.pygobject3}/lib/python3.*/site-packages
  '';
}
