#!/usr/bin/env python3

import sys
import pytesseract as p
from PIL import Image

p.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

print(p.image_to_string(Image.open(sys.argv[1]), lang="slk"))
print("asd")
