from conans import ConanFile, CMake, tools
import os


class SimpleAmqpClientConan(ConanFile):
    name = "SimpleAmqpClient"
    version = "2.5.0-pre1"
    license = "MIT"
    description = "SimpleAmqpClient is an easy-to-use C++ wrapper around the rabbitmq-c C library"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=True", "fPIC=True"
    requires = ("rabbitmq-c/0.6.0@dbely/testing", "boost/1.66.0@conan/stable")
    generators = "cmake"

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if self.settings.os != "Windows" and self.options.shared:
            self.options["boost"].fPIC = True

    def source(self):
        url = "https://github.com/alanxz/SimpleAmqpClient.git"
        self.run("git clone " + url)
        self.run("cd %s && git checkout %s" % (self.name, "6323892d3e"))
        tools.replace_in_file("%s/CMakeLists.txt" % self.name, "PROJECT(SimpleAmqpClient)",
                              """PROJECT(SimpleAmqpClient)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")
        os.unlink("%s/Modules/FindRabbitmqc.cmake" % self.name)
        tools.replace_in_file("%s/CMakeLists.txt" % self.name,
                              "SET(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Modules)",
                              "list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Modules)")

    def build(self):
        cmake = CMake(self)
        if self.options.shared:
            cmake.definitions['BUILD_SHARED_LIBS'] = True
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install"
        cmake.configure(source_folder=self.name)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst=".", src="install")
        self.copy("*.lib", dst="lib", src="install", keep_path=False)
        self.copy("*.dll", dst="bin", src="install", keep_path=False)
        self.copy("*.pdb", dst="bin", src="install", keep_path=False)
        self.copy("*.so*", dst="lib", src="install", keep_path=False, symlinks=True)
        self.copy("*.dylib", dst="lib", src="install", keep_path=False, symlinks=True)
        self.copy("*.a", dst="lib", src="install", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = [self.name+".2"]
        else:
            self.cpp_info.libs = [self.name]
