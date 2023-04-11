import pathlib
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize


source_files: list[str] = [str(pathlib.Path(__file__).parent/"harvesine.pyx")]
ext_modules = [
    Extension("harvesine", sources=source_files)
]

setup(
    name="harvesine",
    ext_modules=cythonize(ext_modules),
    zip_safe=False,
)

