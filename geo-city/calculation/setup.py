import pathlib
from setuptools import Extension, setup
from Cython.Build import cythonize


source_files: list[str] = [str(pathlib.Path(__file__).parent/"calculation.pyx")]
ext_modules: list[Extension] = [
    Extension("calculation", sources=source_files)
]

setup(
    name="calculation",
    ext_modules=cythonize(ext_modules),
    zip_safe=False,
)




# ext_module_dostuff = Extension(
#     'poc.do_stuff',
#     ['poc/do_stuff.pyx'],
# )
#
# ext_module_helloworld = Extension(
#     'poc.cython_extensions.helloworld',
#     ['poc/cython_extensions/helloworld.pyx', 'poc/cython_extensions/test.c', 'poc/cython_extensions/cvRoberts_dns.c'],
#     include_dirs = ['/usr/local/include'],
#     libraries = ['m', 'sundials_cvodes', 'sundials_nvecserial'],
#     library_dirs = ['/usr/local/lib'],
# )
#
# cython_ext_modules = [
#    ext_module_dostuff,
#    ext_module_helloworld
# ]


# setup (
#   name = "poc",
#   ext_modules = cythonize(cython_ext_modules),
#   packages=['poc', 'poc.cython_extensions'],
# )


# harvesine = Extension(
#     "calc",
#     ["src/harvesine.py"],
#     libraries=["m"]
# )
#
# process = Extension(
#     "proc",
#     ["src/process.pyx"]
# )
#
# ext_modules = [process]
# setup(
#   name="calculation",
#   ext_modules=cythonize(ext_modules),
# )


# source_files: list[str] = [
#     str(pathlib.Path(__file__).parent/"harvesine.py")
# ]
#
# ext_modules = [
#     Extension("harvesine", sources=source_files, libraries=["m"])
# ]
#
# setup(
#     name="harvesine",
#     ext_modules=cythonize(ext_modules),
#     zip_safe=False
# )

