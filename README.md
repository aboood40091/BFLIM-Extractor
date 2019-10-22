# BFLIM Extractor v2.3
Extracts textures from the BFLIM ('FLIM' / .bflim file extension) format used in Wii U games, and saves them as DDS.  
  
Can Also convert DDS files into .bflim files!  

## Requirements:
* Python 3.4 or higher.
* Cython (Optional)
* cx_Freeze. (Optional)

## Supported BFLIM formats:
* GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM
* GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_SRGB
* GX2_SURFACE_FORMAT_TCS_R10_G10_B10_A2_UNORM
* GX2_SURFACE_FORMAT_TCS_R5_G6_B5_UNORM
* GX2_SURFACE_FORMAT_TC_R5_G5_B5_A1_UNORM
* GX2_SURFACE_FORMAT_TC_R4_G4_B4_A4_UNORM
* GX2_SURFACE_FORMAT_TC_R8_UNORM
* GX2_SURFACE_FORMAT_TC_R8_G8_UNORM
* GX2_SURFACE_FORMAT_TC_R4_G4_UNORM
* GX2_SURFACE_FORMAT_T_BC1_UNORM
* GX2_SURFACE_FORMAT_T_BC1_SRGB
* GX2_SURFACE_FORMAT_T_BC2_UNORM
* GX2_SURFACE_FORMAT_T_BC2_SRGB
* GX2_SURFACE_FORMAT_T_BC3_UNORM
* GX2_SURFACE_FORMAT_T_BC3_SRGB
* GX2_SURFACE_FORMAT_T_BC4_UNORM
* GX2_SURFACE_FORMAT_T_BC5_UNORM

## Supported DDS formats:
* ABGR8
* BGR8
* A2RGB10
* RGB565
* A1RGB5
* ARGB4
* L8
* A8
* A8L8
* A4L4
* ETC1
* BC1
* BC2
* BC3
* BC4
* BC5

## Credits:
* AboodXD - Writing this thingy.

## Special thanks to:
* Exzap - Helping with swizzling.