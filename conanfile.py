from conans import ConanFile, AutoToolsBuildEnvironment

class SqlitelibConan(ConanFile):
    name = "sqlite"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "This recipe file used to build and package binaries of sqlite repository"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = { "shared": [ True, False ] }
    default_options = "shared=False"
    generators = "make"

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        self.run("cd .. && autoreconf -fsi ")
        autotools.configure(configure_dir="..",args=["--prefix=${PWD}"])
        autotools.make()
        autotools.install()

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = [ "sqlite" ]
