# Wii U BFLIM Extractor
Extracts textures from the FLIM format used in Wii U games.  
  
Can Also convert .png files into .bflim files!  

# Requirements:
Python 3.4 or higher (If running from source code): https://www.python.org/download/releases/3.4.3/

Pillow (If running from source code): https://pypi.python.org/pypi/Pillow/3.3.1

cx_Freeze (Optional, if running from source code): https://pypi.python.org/pypi/cx_Freeze/4.3.4

Compressonator: https://github.com/GPUOpen-Tools/Compressonator/releases/tag/V2.3.2953

# Supported formats:
* RGBA32 (^l)
* BC1 (DXT1) (^o)
* BC2 (DXT3) (^p)
* BC3 (DXT5) (^q)

# Special thanks to:
Exzap, AddrLib - Helping with swizzling.