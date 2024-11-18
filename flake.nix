{
  description = "Moraxyc's MCDReforged Plugins'";

  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [ ];
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
        "x86_64-darwin"
      ];
      perSystem =
        {
          config,
          self',
          inputs',
          pkgs,
          system,
          ...
        }:
        {
          devShells = {
            default = pkgs.mkShell {
              venvDir = ".venv";
              packages =
                with pkgs;
                [ python312 ]
                ++ (with pkgs.python312Packages; [
                  pip
                  venvShellHook

                  mcdreforged
                ]);
            };
          };
        };
      flake = { };
    };
}
