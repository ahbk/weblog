{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    buildInputs = with pkgs; [
      python310
      poetry
      postgresql
      nodejs
    ];
}
