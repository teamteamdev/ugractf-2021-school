{ buildPythonPackage, pyelftools, zlib, glibc }:

buildPythonPackage {
  name = "hahask";

  buildInputs = [ zlib glibc.static ];

  hardeningDisable = [ "all" ];
}
