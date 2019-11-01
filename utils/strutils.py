# import ctypes
from PIL import ImageFont


def get_text_dimensions(text, fontname, points):
    fontname = fontname.replace(' ', '').lower()
    font = ImageFont.truetype(fontname + '.ttf', points)
    return font.getsize(text)


def getWidestTextDimension(values, fontname, points):
    result = (0, 0)
    for value in values:
        dim = get_text_dimensions(value, fontname, points)
        if dim[0] > result[0]:
            result = dim
    return result[0]


def monthPrettify(month):
    return month[2:] + '/' + month[0:2]
