#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BFLIM Extractor
# Version v2.0
# Copyright © 2016-2017 Stella/AboodXD

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

"""bflim_extract.py: Decode BFLIM images."""

import os
import struct
import sys
import time

try:
    import addrlib_cy as addrlib
except ImportError:
    import addrlib

import dds

try:
    import form_conv_cy as form_conv
except ImportError:
    import form_conv

__author__ = "Stella/AboodXD"
__copyright__ = "Copyright 2016-2017 Stella/AboodXD"
__credits__ = ["Stella/AboodXD", "AddrLib", "Exzap"]

formats = {0x00000000: 'GX2_SURFACE_FORMAT_INVALID',
           0x0000001a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM',
           0x0000041a: 'GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB',
           0x00000019: 'GX2_SURFACE_FORMAT_TCS_R10_G10_B10_A2_UNORM',
           0x00000008: 'GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM',
           0x0000000a: 'GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM',
           0x0000000b: 'GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM',
           0x00000001: 'GX2_SURFACE_FORMAT_TC_R8_UNORM',
           0x00000007: 'GX2_SURFACE_FORMAT_TC_R8_G8_UNORM',
           0x00000002: 'GX2_SURFACE_FORMAT_TC_R4_G4_UNORM',
           0x00000031: 'GX2_SURFACE_FORMAT_T_BC1_UNORM',
           0x00000431: 'GX2_SURFACE_FORMAT_T_BC1_SRGB',
           0x00000032: 'GX2_SURFACE_FORMAT_T_BC2_UNORM',
           0x00000432: 'GX2_SURFACE_FORMAT_T_BC2_SRGB',
           0x00000033: 'GX2_SURFACE_FORMAT_T_BC3_UNORM',
           0x00000433: 'GX2_SURFACE_FORMAT_T_BC3_SRGB',
           0x00000034: 'GX2_SURFACE_FORMAT_T_BC4_UNORM',
           0x00000035: 'GX2_SURFACE_FORMAT_T_BC5_UNORM'
           }

BCn_formats = [0x31, 0x431, 0x32, 0x432, 0x33, 0x433, 0x34, 0x35]

# ----------\/-Start of BFLIM Extracting section-\/------------- #
class FLIMData:
    pass

class FLIMHeader(struct.Struct):
    def __init__(self, bom):
        super().__init__(bom + '4s2H2IH2x')

    def data(self, data, pos):
        (self.magic,
        self.endian,
        self.size_,
        self.version,
        self.fileSize,
        self.numBlocks) = self.unpack_from(data, pos)

class imagHeader(struct.Struct):
    def __init__(self, bom):
        super().__init__(bom + '4sI3H2BI')

    def data(self, data, pos):
        (self.magic,
        self.infoSize,
        self.width,
        self.height,
        self.alignment,
        self.format_,
        self.swizzle_tileMode,
        self.imageSize) = self.unpack_from(data, pos)

def computeSwizzleTileMode(z):
    if type(z) == int:
        z = bin(z)[2:].zfill(8)

        tileMode = int(z[3:], 2)

        if tileMode in [1, 2, 3, 16]:
            s = 0
        else:
            s = 0xd0000 
        s |= int(z[:3], 2) << 8

        return s, tileMode

    if type(z) == tuple:
        z = bin(z[0])[2:].zfill(3) + bin(z[1])[2:].zfill(5)
        return int(z, 2)
        

def readFLIM(f):
    flim = FLIMData()

    pos = len(f) - 0x28

    if f[pos+4:pos+6] == b'\xFF\xFE':
        bom = '<'
    elif f[pos+4:pos+6] == b'\xFE\xFF':
        bom = '>'

    header = FLIMHeader(bom)
    header.data(f, pos)
    
    if header.magic != b'FLIM':
        raise ValueError("Invalid file header!")

    pos += header.size

    info = imagHeader(bom)
    info.data(f, pos)

    if info.magic != b'imag':
        raise ValueError("Invalid imag header!")

    flim.width = info.width
    flim.height = info.height

    if info.format_ == 0x00:
        flim.format = 0x01
        flim.compSel = [0, 0, 0, 5]

    elif info.format_ == 0x01:
        flim.format = 0x01
        flim.compSel = [5, 5, 5, 0]

    elif info.format_ == 0x02:
        flim.format = 0x02
        flim.compSel = [0, 0, 0, 1]

    elif info.format_ == 0x03:
        flim.format = 0x07
        flim.compSel = [0, 0, 0, 1]

    elif info.format_ in [0x05, 0x19]:
        flim.format = 0x08
        flim.compSel = [0, 1, 2, 5]

    elif info.format_ == 0x06:
        flim.format = 0x1a
        flim.compSel = [0, 1, 2, 5]

    elif info.format_ == 0x07:
        flim.format = 0x0a
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x08:
        flim.format = 0x0b
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x09:
        flim.format = 0x1a
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x0a:
        flim.format = 0x31
        flim.format_ = "ETC1"
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x0C:
        flim.format = 0x31
        flim.format_ = "BC1"
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x0D:
        flim.format = 0x32
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x0E:
        flim.format = 0x33
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ in [0x0F, 0x10]:
        flim.format = 0x34
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x11:
        flim.format = 0x35
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x14:
        flim.format = 0x41a
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x15:
        flim.format = 0x431
        flim.format_ = "BC1"
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x16:
        flim.format = 0x432
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x17:
        flim.format = 0x433
        flim.compSel = [0, 1, 2, 3]

    elif info.format_ == 0x18:
        flim.format = 0x19
        flim.compSel = [0, 1, 2, 3]

    else:
        print("")
        print("Unsupported texture format: " + hex(info.format_))
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    flim.imageSize = info.imageSize

    # Calculate swizzle and tileMode
    flim.swizzle, flim.tileMode = computeSwizzleTileMode(info.swizzle_tileMode)

    flim.alignment = info.alignment

    surfOut = addrlib.getSurfaceInfo(flim.format, flim.width, flim.height, 1, 1, flim.tileMode, 0, 0)

    if surfOut.depth != 1:
        print("")
        print("Unsupported depth!")
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    flim.pitch = surfOut.pitch

    flim.data = f[:info.imageSize]

    flim.surfOut = surfOut

    if flim.format in BCn_formats:
        flim.realSize = ((flim.width + 3) >> 2) * ((flim.height + 3) >> 2) * (addrlib.surfaceGetBitsPerPixel(flim.format) // 8)
    else:
        flim.realSize = flim.width * flim.height * (addrlib.surfaceGetBitsPerPixel(flim.format) // 8)

    return flim

def get_deswizzled_data(flim):
    if flim.format == 0x01:
        format_ = 61
    elif flim.format == 0x02:
        format_ = 112
    elif flim.format == 0x07:
        format_ = 49
    elif flim.format == 0x08:
        format_ = 85
    elif flim.format == 0x0a:
        format_ = 86
    elif flim.format == 0x0b:
        format_ = 115
    elif flim.format in [0x1a, 0x41a]:
        format_ = 28
    elif flim.format == 0x19:
        format_ = 24
    elif flim.format in [0x31, 0x431]:
        format_ = flim.format_
    elif flim.format in [0x32, 0x432]:
        format_ = "BC2"
    elif flim.format in [0x33, 0x433]:
        format_ = "BC3"
    elif flim.format == 0x34:
        format_ = "BC4U"
    elif flim.format == 0x35:
        format_ = "BC5U"

    result = addrlib.deswizzle(flim.width, flim.height, flim.surfOut.height, flim.format, flim.surfOut.tileMode, flim.swizzle, flim.pitch, flim.surfOut.bpp, flim.data)

    if flim.format in BCn_formats:
        size = ((flim.width + 3) >> 2) * ((flim.height + 3) >> 2) * (addrlib.surfaceGetBitsPerPixel(flim.format) >> 3)
    else:
        size = flim.width * flim.height * (addrlib.surfaceGetBitsPerPixel(flim.format) >> 3)

    result = result[:size]

    if flim.format == 0xa:
        result = form_conv.toDDSrgb5a1(result)
    elif flim.format == 0xb:
        result = form_conv.toDDSrgba4(result)

    hdr = dds.generateHeader(1, flim.width, flim.height, format_, flim.compSel, size, flim.format in BCn_formats)

    return hdr, result

def warn_color():
    print("")
    print("Warning: colors might mess up!!")

def writeFLIM(f, tileMode, swizzle_, SRGB):
    width, height, format_, fourcc, dataSize, compSel, numMips, data = dds.readDDS(f, SRGB)

    if 0 in [width, dataSize] and data == []:
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    data = data[:dataSize]

    bpp = addrlib.surfaceGetBitsPerPixel(format_) >> 3

    alignment = 512 * bpp

    surfOut = addrlib.getSurfaceInfo(format_, width, height, 1, 1, tileMode, 0, 0)

    padSize = surfOut.surfSize - dataSize
    data += padSize * b"\x00"

    if surfOut.depth != 1:
        print("")
        print("Unsupported depth!")
        print("Exiting in 5 seconds...")
        time.sleep(5)
        sys.exit(1)

    z = (swizzle_, tileMode)
    swizzle_tileMode = computeSwizzleTileMode(z)

    if tileMode in [1, 2, 3, 16]:
        s = 0
    else:
        s = 0xd0000

    s |= swizzle_ << 8

    print("")
    print("  width           = " + str(width))
    print("  height          = " + str(height))
    print("  format          = " + formats[format_])
    print("  imageSize       = " + str(len(data)))
    print("  tileMode        = " + str(tileMode))
    print("  swizzle         = " + str(s) + ", " + hex(s))
    print("  alignment       = " + str(alignment))
    print("  pitch           = " + str(surfOut.pitch))
    print("")
    print("  bits per pixel  = " + str(bpp << 3))
    print("  bytes per pixel = " + str(bpp))
    print("  realSize        = " + str(dataSize))

    swizzled_data = addrlib.swizzle(width, height, surfOut.height, format_, surfOut.tileMode, s, surfOut.pitch, surfOut.bpp, data)

    if format_ == 1:
        if 3 in compSel:
            format_ = 1
        else:
            format_ = 0

    elif format_ == 0x1a:
        if 5 in compSel:
            format_ = 6
        else:
            format_ = 9

    elif format_ == 0x31:
        if fourcc == b'ETC1':
            format_ = 0xa
        else:
            format_ = 0xc

    else:
        fmt = {7: 3, 8: 5, 0xa: 7, 0xb: 8, 0x32: 0xd, 0x33: 0xe, 0x34: 0x10, 0x35: 0x11, 0x41a: 0x14, 0x431: 0x15, 0x432: 0x16, 0x433: 0x17, 0x19: 0x18}
        format_ = fmt[format_]

    if format_ == 0:
        if compSel not in [[0, 0, 0, 5], [0, 4, 4, 5]]:
            warn_color()

    elif format_ == 1:
        if compSel != [4, 4, 4, 5]:
            warn_color()

    elif format_ in [2, 3]:
        if compSel not in [[0, 0, 0, 1], [0, 4, 4, 1]]:
            warn_color()

    elif format_ in [5, 6]:
        if compSel != [0, 1, 2, 5]:
            warn_color()

    else:
        if compSel != [0, 1, 2, 3]:
            warn_color()

    head_struct = FLIMHeader('>')
    head = head_struct.pack(b"FLIM", 0xFEFF, 0x14, 0x2020000, len(swizzled_data) + 0x28, 1)

    img_head_struct = imagHeader('>')
    imag_head = img_head_struct.pack(b"imag", 16, width, height, alignment, format_, swizzle_tileMode, len(swizzled_data))

    output = swizzled_data + head + imag_head

    return output

def printInfo():
    print("")
    print("Usage:")
    print("  bflim_extract [option...] input")
    print("")
    print("Options:")
    print(" -o <output>           Output file, if not specified, the output file will have the same name as the intput file")
    print("")
    print("DDS to BFLIM options:")
    print(" -tileMode <tileMode>  tileMode (4 is the default)")
    print(" -swizzle <swizzle>    the intial swizzle value, a value from 0 to 7 (0 is the default)")
    print(" -SRGB <n>             1 if the desired destination format is SRGB, else 0 (0 is the default)")
    print("")
    print("Supported BFLIM formats:")
    print(" - GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM")
    print(" - GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB")
    print(" - GX2_SURFACE_FORMAT_TCS_R10_G10_B10_A2_UNORM")
    print(" - GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM")
    print(" - GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM")
    print(" - GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM")
    print(" - GX2_SURFACE_FORMAT_TC_R8_UNORM")
    print(" - GX2_SURFACE_FORMAT_TC_R8_G8_UNORM")
    print(" - GX2_SURFACE_FORMAT_TC_R4_G4_UNORM")
    print(" - GX2_SURFACE_FORMAT_T_BC1_UNORM")
    print(" - GX2_SURFACE_FORMAT_T_BC1_SRGB")
    print(" - GX2_SURFACE_FORMAT_T_BC2_UNORM")
    print(" - GX2_SURFACE_FORMAT_T_BC2_SRGB")
    print(" - GX2_SURFACE_FORMAT_T_BC3_UNORM")
    print(" - GX2_SURFACE_FORMAT_T_BC3_SRGB")
    print(" - GX2_SURFACE_FORMAT_T_BC4_UNORM")
    print(" - GX2_SURFACE_FORMAT_T_BC5_UNORM")
    print("")
    print("Supported DDS formats:")
    print(" - ABGR8")
    print(" - BGR8")
    print(" - A2BGR10")
    print(" - RGB565")
    print(" - A1RGB5")
    print(" - ARGB4")
    print(" - L8")
    print(" - A8")
    print(" - A8L8")
    print(" - A4L4")
    print(" - ETC1")
    print(" - BC1")
    print(" - BC2")
    print(" - BC3")
    print(" - BC4")
    print(" - BC5")
    print("")
    print("Exiting in 5 seconds...")
    time.sleep(5)
    sys.exit(1)

def main():
    print("BFLIM Extractor v2.0")
    print("(C) 2016-2017 Stella/AboodXD")
    
    input_ = sys.argv[-1]

    if not (input_.endswith('.bflim') or input_.endswith('.dds')):
        printInfo()

    toFLIM = False

    if input_.endswith('.dds'):
        toFLIM = True

    if "-o" in sys.argv:
        output_ = sys.argv[sys.argv.index("-o") + 1]
    else:
        output_ = os.path.splitext(input_)[0] + (".bflim" if toFLIM else ".dds")

    print("")
    print('Converting: ' + input_)

    if toFLIM:
        if "-tileMode" in sys.argv:
            tileMode = int(sys.argv[sys.argv.index("-tileMode") + 1], 0)
        else:
            tileMode = 4

        if "-swizzle" in sys.argv:
            swizzle = int(sys.argv[sys.argv.index("-swizzle") + 1], 0)
        else:
            swizzle = 0

        if "-SRGB" in sys.argv:
            SRGB = int(sys.argv[sys.argv.index("-SRGB") + 1], 0)
        else:
            SRGB = 0

        if SRGB > 1 or not 0 <= tileMode <= 16 or not 0 <= swizzle <= 7:
            printInfo()

        data = writeFLIM(input_, tileMode, swizzle, SRGB)

        with open(output_, "wb+") as output:
            output.write(data)

    else:
        with open(input_, "rb") as inf:
            inb = inf.read()

        flim = readFLIM(inb)

        print("")
        print("  width           = " + str(flim.width))
        print("  height          = " + str(flim.height))
        if flim.format in formats:
            print("  format          = " + formats[flim.format])
        else:
            print("  format          = " + hex(flim.format))
        print("  imageSize       = " + str(flim.imageSize))
        print("  tileMode        = " + str(flim.tileMode))
        print("  swizzle         = " + str(flim.swizzle) + ", " + hex(flim.swizzle))
        print("  alignment       = " + str(flim.alignment))
        print("  pitch           = " + str(flim.pitch))
        bpp = addrlib.surfaceGetBitsPerPixel(flim.format)
        print("")
        print("  bits per pixel  = " + str(bpp))
        print("  bytes per pixel = " + str(bpp // 8))
        print("  realSize        = " + str(flim.realSize))
        
        name = os.path.splitext(sys.argv[1])[0]

        hdr, data = get_deswizzled_data(flim)

        with open(output_, "wb+") as output:
            output.write(hdr)
            output.write(data)

    print('')
    print('Finished converting: ' + output_)

if __name__ == '__main__': main()
