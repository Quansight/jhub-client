{ pkgs ? import <nixpkgs> { }, pythonPackages ? pkgs.python3Packages }:

pkgs.mkShell {
  buildInputs = with pythonPackages; [
    pkgs.docker-compose

    jupyterhub
    jupyterlab
    aiohttp
    yarl

    pytest
    pytest-asyncio
  ];
}
