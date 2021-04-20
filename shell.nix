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
    black
    flake8
  ];

  shellHook = ''
    export JUPYTERHUB_API_TOKEN=GiJ96ujfLpPsq7oatW1IJuER01FbZsgyCM0xH6oMZXDAV6zUZsFy3xQBZakSBo6P
  '';
}
