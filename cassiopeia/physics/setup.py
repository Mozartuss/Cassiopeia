from distutils.core import setup
from distutils.extension import Extension

import Cython.Compiler.Options
import numpy
from Cython.Distutils import build_ext

Cython.Compiler.Options.annotate = True


ext_modules = [
    Extension(
    name="cython_calculation",
    sources=["cython_calculation.pyx"],
    libraries=["m"],
    extra_compile_args=["-O3", "-ffast-math"]),
    Extension(
    name="init_planets",
    sources=["init_planets.pyx"],
    libraries=["m"],
    extra_compile_args=["-O3", "-ffast-math"])
]

setup(
    name='Cassiopeia',
    cmdclass={'build_ext': build_ext},
    include_dirs=[numpy.get_include()],
    ext_modules=ext_modules,
)
