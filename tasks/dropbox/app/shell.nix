{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      python3Packages.flask
      python3.pkgs.gunicorn
      bubblewrap
    ];
}

