{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix.url = "github:nix-community/poetry2nix";
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux";
      inherit (poetry2nix.legacyPackages.${system}) mkPoetryEnv mkPoetryApplication;
      pkgs = import nixpkgs { inherit system; };

      buildInputs = with pkgs; [
	poetry2nix.packages.${system}.poetry
	postgresql
      ];

      buildInputsApp = buildInputs ++ [ (mkPoetryApplication { projectDir = ./be; }) ];
      buildInputsEnv = buildInputs ++ (with pkgs; [
	(mkPoetryEnv { projectDir = ./be; })
	black
      ]);
    in {
      packages.${system}.default = pkgs.stdenv.mkDerivation {
        name = "weblog";
	buildInputs = buildInputsApp;
      };
      devShells.${system}.default = pkgs.mkShell {
        packages = buildInputsEnv;
        shellHook = ''
	  source .env
	  export E="asdf"
	  '';
      };
    };
}
