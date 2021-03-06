import os
from conans import ConanFile, CMake, tools

class SqlitelibConan(ConanFile):
    name = "sqlite3"
    version = "3.26.0"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "https://github.com/elear-solutions/sqlite"
    homepage = "https://www.sqlite.org"
    description = "Self-contained, serverless, in-process SQL database engine."
    topics = ("sqlite", "database", "sql", "serverless")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = {"shared": [True, False],
               "fPIC": [True, False],
               "threadsafe": [0, 1, 2],
               "enable_column_metadata": [True, False],
               "enable_explain_comments": [True, False],
               "enable_fts3": [True, False],
               "enable_fts4": [True, False],
               "enable_fts5": [True, False],
               "enable_json1": [True, False],
               "enable_rtree": [True, False],
               "omit_load_extension": [True, False],
               "enable_memstatus": [0, 1]
               }
    default_options = {"shared": False,
                       "fPIC": True,
                       "threadsafe": 1,
                       "enable_column_metadata": False,
                       "enable_explain_comments": False,
                       "enable_fts3": False,
                       "enable_fts4": False,
                       "enable_fts5": False,
                       "enable_json1": True,
                       "enable_rtree": False,
                       "omit_load_extension": False,
                       "enable_memstatus": 0
                       }

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["THREADSAFE"] = self.options.threadsafe
        cmake.definitions["ENABLE_COLUMN_METADATA"] = self.options.enable_column_metadata
        cmake.definitions["ENABLE_EXPLAIN_COMMENTS"] = self.options.enable_explain_comments
        cmake.definitions["ENABLE_FTS3"] = self.options.enable_fts3
        cmake.definitions["ENABLE_FTS4"] = self.options.enable_fts4
        cmake.definitions["ENABLE_FTS5"] = self.options.enable_fts5
        cmake.definitions["ENABLE_JSON1"] = self.options.enable_json1
        cmake.definitions["ENABLE_RTREE"] = self.options.enable_rtree
        cmake.definitions["OMIT_LOAD_EXTENSION"] = self.options.omit_load_extension
        cmake.definitions["ENABLE_MEMSTATUS"] = self.options.enable_memstatus
        cmake.definitions["HAVE_FDATASYNC"] = True
        cmake.definitions["HAVE_GMTIME_R"] = True
        cmake.definitions["HAVE_LOCALTIME_R"] = True
        cmake.definitions["HAVE_POSIX_FALLOCATE"] = True
        cmake.definitions["HAVE_STRERROR_R"] = True
        cmake.definitions["HAVE_USLEEP"] = True
        if self.settings.os == "Windows":
            cmake.definitions["HAVE_LOCALTIME_R"] = False
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        if tools.is_apple_os(self.settings.os):
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        if self.settings.os == "Android":
            cmake.definitions["HAVE_POSIX_FALLOCATE"] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="package/include")
        self.copy("*", dst="lib", src="package/lib")

    def package_info(self):
        self.cpp_info.libs = [ "sqlite3" ]
