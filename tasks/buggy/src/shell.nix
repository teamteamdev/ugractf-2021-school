{ pkgs ? import <nixpkgs> { } }:

pkgs.python3.pkgs.callPackage ./. { }
