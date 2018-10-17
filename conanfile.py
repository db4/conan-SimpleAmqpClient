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
    requires = ("rabbitmq-c/0.6.0@dbely/testing", "boost/[>=1.66.0]@conan/stable")
    generators = "cmake", "cmake_find_package"

    @property
    def src_dir(self):
        return "%s-%s" % (self.name, self.version)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("shared")
            self.options.remove("fPIC")

    def configure(self):
        if self.settings.os != "Windows" and self.options.shared:
            self.options["boost"].fPIC = True

    def source(self):
        url = "https://github.com/alanxz/SimpleAmqpClient.git"
        self.run("git clone %s %s" % (url, self.src_dir))
        self.run("cd %s && git checkout %s" % (self.src_dir, "6323892d3e"))
        cmakelist_tst = os.path.join(self.src_dir, "CMakeLists.txt")
        tools.replace_in_file(cmakelist_tst, "PROJECT(SimpleAmqpClient)",
                              """PROJECT(SimpleAmqpClient)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")
        os.unlink("%s/Modules/FindRabbitmqc.cmake" % self.src_dir)
        tools.replace_in_file(cmakelist_tst,
                              "SET(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Modules)",
                              "list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/Modules)")
        tools.replace_in_file(cmakelist_tst, "${Rabbitmqc_SSL_ENABLED}", "ON")
        tools.replace_in_file(cmakelist_tst, "Rabbitmqc_LIBRARY", "rabbitmq-c_LIBRARIES")
        tools.replace_in_file(cmakelist_tst, "Rabbitmqc", "rabbitmq-c")
        tools.replace_in_file(cmakelist_tst, "Boost", "boost")

    def build(self):
        cmake = CMake(self)
        if self.settings.os != "Windows":
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC
        else:
            cmake.definitions['BUILD_SHARED_LIBS'] = True
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "install"
        cmake.configure(source_folder=self.src_dir)
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
