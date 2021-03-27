{ buildPythonPackage, pyelftools, zlib, glibc }:

buildPythonPackage {
  name = "hahask";

  propagatedBuildInputs = [ pyelftools ];
  buildInputs = [ zlib zlib.static glibc.static ];

  hardeningDisable = [ "all" ];
}
