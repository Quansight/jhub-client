{
  description = "jhub-client";

  inputs = {
    nixpkgs = { url = "github:nixos/nixpkgs/nixpkgs-unstable"; };
  };

  outputs = inputs@{ self, nixpkgs, ... }: {
    devShell.x86_64-linux =
      let
        pkgs = import nixpkgs { system = "x86_64-linux"; };
        pythonPackages = pkgs.python3Packages;
      in pkgs.mkShell {
        buildInputs = [
          pkgs.docker-compose

          # development
          pythonPackages.aiohttp
          pythonPackages.yarl
          pythonPackages.pytest
          pythonPackages.pytest-asyncio
          pythonPackages.black
          pythonPackages.flake8
        ];

        shellHook = ''
          export JUPYTERHUB_API_TOKEN=GiJ96ujfLpPsq7oatW1IJuER01FbZsgyCM0xH6oMZXDAV6zUZsFy3xQBZakSBo6P
          export PYTHONPATH=$PWD:$PYTHONPATH
        '';
      };
  };
}
