#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, shutil
from conans import ConanFile, CMake, tools
from conans.errors import ConanException


class UvLinktConan(ConanFile):
    name = "uv_link_t"
    version = "1.0.5"
    description = "Chainable libuv streams"
    url = "https://github.com/alekseevx/conan-uv_link_t"
    license = "MIT"
    exports_sources = "CMakeLists.txt"
    settings = "os", "arch", "compiler", "build_type"
    generators = "cmake"
    options = {}
    

    def source(self):
        shutil.rmtree("src", ignore_errors=True)
                    
        tools.get(
            url="https://github.com/indutny/uv_link_t/archive/v{ver}.tar.gz".format(ver=self.version),
            sha256="1fb573ba0f0f7eb67dd603853e0df13aca454d4f4cd7433f7f5b21036aaa4a1d"
        )
        source_dir = "{name}-{version}".format(name=self.name, version=self.version)
        shutil.move(source_dir, "src")
        shutil.copy(src="CMakeLists.txt", dst="src")

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.compiler == "Visual Studio" and int(str(self.settings.compiler.version)) < 14:
            raise ConanException("Visual Studio >= 14 (2015) is required")

    def requirements(self):
        self.requires("cmake_installer/3.10.0@conan/stable", private=True)
        self.requires("libuv/1.15.0@bincrafters/stable")

    def build(self):
        shutil.rmtree("build", ignore_errors=True)
        os.mkdir("build")

        cmake = CMake(self)
        cmake.verbose = True        
        cmake.configure(source_dir="../src", build_dir="build")
        cmake.build()

    def package(self):
        self.copy("src/README.md", dst=".", keep_path=False)
        self.copy("*.h", src="src/include", dst="include", keep_path=False)
        self.copy("*.a", src="build/lib", dst="lib", keep_path=False)
        self.copy("*.lib", src="build/lib", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

