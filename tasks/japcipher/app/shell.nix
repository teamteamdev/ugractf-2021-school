{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      python3Packages.aiohttp
      python3Packages.aiohttp-session
      python3Packages.aiohttp-jinja2
      python3Packages.cryptography
    ];
}
