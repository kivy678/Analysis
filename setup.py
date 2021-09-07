# -*- coding:utf-8 -*-

##################################################################################################

import os
import shutil

import platform

from distutils.core import setup, Extension

Join = os.path.join

##################################################################################################

if os.path.exists("build"):
    shutil.rmtree("build")

system_os = platform.system()
arch, _ = platform.architecture()

##################################################################################################

NLIB_DIR = Join(os.path.dirname(os.path.realpath(__file__)), 'module', 'Nlib')
CAPSTONE_PATH = Join(NLIB_DIR, 'capstone', system_os, f'x{arch[:2]}')

INCLUDE_NLIB_PATH = Join(NLIB_DIR, 'include')
CAPSTONE_INCLUDE_PATH = Join(CAPSTONE_PATH, 'include')

CAPSTONE_LIB_PATH = Join(CAPSTONE_PATH, 'lib')
CAPSTONE_LIB_NAME_PATH = Join(CAPSTONE_PATH, 'lib', 'capstone')

##################################################################################################

capstoneM = Extension(
    'disassemble',
    define_macros=[("MAJOR_VERSION", "1"), ("MINOR_VERSION", "0")],
    include_dirs=[INCLUDE_NLIB_PATH, CAPSTONE_INCLUDE_PATH],
    library_dirs=[CAPSTONE_LIB_PATH],
    libraries = [CAPSTONE_LIB_NAME_PATH],
    sources=['module/Nlib/disassemble.c', ],
    language="c",
    extra_compile_args=["-std=c++11", "-Wall", "-O3"],
)

##################################################################################################

elfM = Extension(
    'elfformat',
    define_macros=[("MAJOR_VERSION", "1"), ("MINOR_VERSION", "0")],
    include_dirs=[INCLUDE_NLIB_PATH],
    sources=['module/Nlib/elfformat.cpp',
             'module/Nlib/module.cpp',
             'module/Nlib/parser.cpp',
             'module/Nlib/heapfree.cpp',
             'module/Nlib/getgot.cpp'],
    language="c++",
    extra_compile_args=["-std=c++11", "-Wall", "-O2"],
)

##################################################################################################

setup(
    name="AndroidTool",
    version="0.9",
    description="AndroidTool",
    author="Kivy",
    author_email="kivy678@gmail.com",
    url="",
    ext_modules=[capstoneM, elfM]
)
##################################################################################################
