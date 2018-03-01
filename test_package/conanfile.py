from conans import ConanFile, CMake, tools, RunEnvironment
import os

class RabbitMQTestConan(ConanFile):
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "gtest/1.8.0@bincrafters/stable"

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is in "test_package"
        cmake.configure()
        cmake.build()

    def test(self):
        if not tools.cross_building(self.settings):
            env_build = RunEnvironment(self)
            with tools.environment_append(env_build.vars):
                os.chdir("bin")
                if self.settings.os != "Windows":
                    # Work around OSX security restrictions
                    self.run("DYLD_LIBRARY_PATH=%s ./test" % os.environ['DYLD_LIBRARY_PATH'])
                else:
                    self.run("test")
