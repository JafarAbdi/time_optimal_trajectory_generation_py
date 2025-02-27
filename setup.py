import sysconfig
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import subprocess
import sys
from pathlib import Path


# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

        debug = int(os.environ.get("DEBUG", 0)) if self.debug is None else self.debug
        cfg = "Debug" if debug else "Release"

        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_BUILD_TYPE={cfg}",  # not used on MSVC, but no harm
            f"-DPython_EXECUTABLE={sys.executable}",
            f"-DPython_INCLUDE_DIRS={sysconfig.get_paths()['include']}",
            f"-DPython_LIBRARIES={sysconfig.get_paths()['stdlib']}",
        ]

        build_temp = os.path.join(self.build_temp, ext.name)
        if not os.path.exists(build_temp):
            os.makedirs(build_temp)

        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_temp)
        subprocess.check_call(["cmake", "--build", "."], cwd=build_temp)


setup(
    name="time_optimal_trajectory_generation_py",
    version="0.0.1",
    ext_modules=[CMakeExtension("time_optimal_trajectory_generation_py", ".")],
    cmdclass={"build_ext": CMakeBuild},
)
