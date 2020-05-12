from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("mymodule1",  ["essentials.py"]),
]

for e in ext_modules:
    e.cython_directives = {'language_level': "3"}

setup(
    name = 'Cythoning 69Essentials',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
