from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension(
        '*',
        [ "fastBPE/fastBPE.pyx" ],
        language='c++',
        extra_compile_args=[
            "-std=c++11", "-stdlib=libc++", "-Ofast", "-pthread"
        ],
    ),
]

setup(
    name = 'fastBPE',
    ext_package = '',
    ext_modules = cythonize(
        extensions,
        language='c++'
    ),
    packages=[
        'fastBPE',
    ],
    install_requires=[
        'Cython'
    ]
)
