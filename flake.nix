{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      buildInputs = with pkgs; [
        poetry
	nodejs
      ];

      buildInputsApp = buildInputs ++ [
      ];

      buildInputsEnv = buildInputs ++ (with pkgs; [
	black
	postgresql
	nodePackages.typescript-language-server
	nodePackages.typescript
	nodePackages.svelte-language-server
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
