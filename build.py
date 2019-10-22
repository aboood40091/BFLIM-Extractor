#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFLIM Extractor
# Version v2.3
# Copyright © 2016-2019 AboodXD

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

import os
import shutil
import sys

from cx_Freeze import setup, Executable

version = '2.3'

# Pick a build directory
dir_ = 'bflim_extract v' + version

# Add the "build" parameter to the system argument list
if 'build' not in sys.argv:
    sys.argv.append('build')

# Clear the directory
print('>> Clearing/creating directory...')

if os.path.isdir(dir_):
    shutil.rmtree(dir_)

os.makedirs(dir_)

print('>> Directory ready!')

setup(
    name='BFLIM Extractor',
    version=version,
    description='Wii U BFLIM Extractor',
    author="AboodXD",
    options={
        'build_exe': {
            'build_exe': dir_,
            'optimize': 2,
            'silent': True,
        },
    },
    executables=[
        Executable(
            'bflim_extract.py',
        ),
    ],
)

print('>> Attempting to copy required files...')
shutil.copy('COPYING', dir_)
shutil.copy('README.md', dir_)
print('>> Files copied!')

print('>> BFLIM Extractor has been frozen to "%s"!' % dir_)
