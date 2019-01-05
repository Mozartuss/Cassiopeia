from distutils.core import setup
from distutils.extension import Extension

import Cython.Compiler.Options
import numpy
from Cython.Distutils import build_ext

Cython.Compiler.Options.annotate = True

ext_modules = [Extension(
    name="cython_calculation",
    sources=["cython_calculation.pyx"],
    extra_compile_args=["-ffast-math"],
    define_macros=[('CYTHON_TRACE', '1')])]

setup(
    name='cython_calculation',
    cmdclass={'build_ext': build_ext},
    include_dirs=[numpy.get_include()],
    ext_modules=ext_modules,

)
