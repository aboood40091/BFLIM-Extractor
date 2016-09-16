#!/usr/bin/env python

# BFLIM Extractor
# Version v1.2
# Copyright © 2016 AboodXD

# This file is part of BFLIM Extractor.

# BFLIM Extractor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# BFLIM Extractor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""build.py: Build an executable for BFLIM Extractor."""

import os, shutil, sys
from cx_Freeze import setup, Executable

version = 'v1.2'

# Pick a build directory
dir_ = 'bflim_extract ' + version

# Add the "build" parameter to the system argument list
if 'build' not in sys.argv:
    sys.argv.append('build')

# Clear the directory
print('>> Clearing/creating directory...')
if os.path.isdir(dir_): shutil.rmtree(dir_)
os.makedirs(dir_)
print('>> Directory ready!')

# exclude QtWebKit to save space, plus Python stuff we don't use
excludes = ['doctest', 'pdb', 'unittest', 'difflib', 'inspect',
    'os2emxpath', 'posixpath', 'optpath', 'locale', 'calendar',
    'select', 'multiprocessing', 'ssl',
    'PyQt5.QtWebKit', 'PyQt5.QtNetwork']

setup(
    name = 'bflim_extract',
    version = version,
    description = 'Wii U BFLIM decoder',
    options={
        'build_exe': {
            'excludes': excludes,
            'build_exe': dir_,
            },
        },
    executables = [
        Executable(
            'bflim_extract.py',
            ),
        ],
    )

print('>> Attempting to copy required files...')
shutil.copy('COPYING', dir_)
shutil.copy('README.md', dir_)
print('>> Files copied!')

print('>> BFLIM Extractor has been frozen to %s !' % dir_)
