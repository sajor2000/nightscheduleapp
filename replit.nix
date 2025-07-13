{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.python310Packages.pip
    pkgs.python310Packages.virtualenv
    pkgs.postgresql_14
    pkgs.nodejs-18_x
    pkgs.nodePackages.npm
  ];
  env = {
    PYTHONBIN = "${pkgs.python310}/bin/python3.10";
    LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.postgresql_14
    ];
  };
}