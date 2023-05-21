{ pkgs ? import <nixpkgs> {} }:
  let
      neovimPythonPackages = p: with p; [
                  jedi
                  flake8
                  black
                  pylint
                 ];
      neovim = pkgs.neovim.override {
                          extraPython3Packages = neovimPythonPackages;
                          withPython3 = true;
                          withNodeJs = true;
                          configure = {
                              customRC = builtins.readFile ./init.vim;
                              plugins = with pkgs.vimPlugins;  [
                                  nerdtree
                                  coc-nvim
                                  coc-python
                              ];
                          };
                     };
  in
  pkgs.mkShell {
    buildInputs = with pkgs; [
      python310
      poetry
      postgresql
      nodejs
      yarn
      neovim
    ];
  }
