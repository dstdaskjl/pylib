import numpy as np
from PIL import Image, ImageEnhance
from typing import Union


#  (0,0) starts from the top-left corner

def brighten_dark_spots(filepath: str) -> np.ndarray:
    image = Image.open(filepath)
    h, s, v = image.convert('HSV').split()
    new_v = v.point(lambda i: i + int(30 * (255 - i) / 255))
    output = Image.merge(mode="HSV", bands=(h, s, new_v)).convert('RGB')
    return np.asarray(output)

#  https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
def convert(src: str, mode: str) -> Image.Image:
    return Image.open(src).convert(mode=mode)

def crop(src: str, top_left: tuple, bottom_right: tuple) -> Image.Image:
    return Image.open(src).crop(*top_left, *bottom_right)

def flip_left_right(src: str) -> Image.Image:
    return Image.open(src).transpose(method=Image.FLIP_LEFT_RIGHT)

def flip_top_bottom(src: str) -> Image.Image:
    return Image.open(src).transpose(method=Image.FLIP_TOP_BOTTOM)

def from_array(array: np.ndarray, mode=None) -> Image.Image:
    return Image.fromarray(array, mode)

def get_colors(src: str) -> list:
    return Image.open(src).getcolors()

def get_pixel(src: str, coord: tuple) -> Union[int, tuple]:
    return Image.open(src).getpixel(xy=coord)

def get_size(src: str) -> tuple:
    return Image.open(src).size

def enhance(src: str, factor: float) -> Image.Image:
    image = Image.open(src)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(factor=factor)
    return image

def make_square(src: str, size=0, fill_color=(0, 0, 0)) -> Image.Image:
    image = Image.open(src)
    x, y = image.size
    if not size:
        size = max(x, y)
    new_image = Image.new('RGB', (size, size), fill_color)
    new_image.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    return new_image

def resize(src: str, size: tuple, resample=Image.ANTIALIAS) -> Image.Image:
    return Image.open(src).resize(size=size, resample=resample)

def rotate(src: str, angle: float, resample=Image.ANTIALIAS, center=None) -> Image.Image:
    return Image.open(src).rotate(angle=angle, resample=resample, center=center)

# https://stackoverflow.com/questions/14415741/what-is-the-difference-between-np-array-and-np-asarray
# np.array always copies an object
# np.asarray copies an object if necessary
def to_array(src: str) -> np.ndarray:
    image = Image.open(src)
    array = np.array(image)
    return array
