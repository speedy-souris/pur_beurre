{pkgs}: {
  deps = [
    pkgs.openssl
    pkgs.libxcrypt
    pkgs.cacert
    pkgs.dos2unix
    pkgs.pkg-config
    pkgs.libffi
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.postgresql
    pkgs.iana-etc
    pkgs.pgadmin4
  ];
}
