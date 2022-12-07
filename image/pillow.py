import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from typing import Union


#  (0,0) starts from the top-left corner

def brighten(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(factor=factor)
    return image

# https://stackoverflow.com/questions/72306585/brighten-only-dark-areas-of-image-in-python
def brighten_dark_spots(image: Image.Image) -> Image.Image:
    h, s, v = image.convert('HSV').split()
    new_v = v.point(lambda i: i + int(20 * (255 - i) / 255))
    image = Image.merge(mode="HSV", bands=(h, s, new_v)).convert('RGB')
    return image

def contrast(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(factor=factor)
    return image

#  https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
def convert(image: Image.Image, mode: str) -> Image.Image:
    return image.convert(mode=mode)

def crop(image: Image.Image, top_left: tuple, bottom_right: tuple) -> Image.Image:
    return image.crop(*top_left, *bottom_right)

def find_edge(image: Image.Image) -> Image.Image:
    return image.convert('L').filter(ImageFilter.FIND_EDGES)

def flip_left_right(image: Image.Image) -> Image.Image:
    return image.transpose(method=Image.FLIP_LEFT_RIGHT)

def flip_top_bottom(image: Image.Image) -> Image.Image:
    return image.transpose(method=Image.FLIP_TOP_BOTTOM)

def from_array(array: np.ndarray, mode=None) -> Image.Image:
    return Image.fromarray(array, mode)

def get_colors(image: Image.Image) -> list:
    return image.getcolors()

def get_pixel(image: Image.Image, coord: tuple) -> Union[int, tuple]:
    return image.getpixel(xy=coord)

def get_size(image: Image.Image) -> tuple:
    return image.size

def make_square(image: Image.Image, size=0, fill_color=(0, 0, 0)) -> Image.Image:
    x, y = image.size
    if not size:
        size = max(x, y)
    new_image = Image.new('RGB', (size, size), fill_color)
    new_image.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    return new_image

def resize(image: Image.Image, size: tuple, resample=Image.ANTIALIAS) -> Image.Image:
    return image.resize(size=size, resample=resample)

def rotate(image: Image.Image, angle: float, resample=Image.ANTIALIAS, center=None) -> Image.Image:
    return image.rotate(angle=angle, resample=resample, center=center)

def sharpen(image: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(factor=factor)
    return image

# https://stackoverflow.com/questions/14415741/what-is-the-difference-between-np-array-and-np-asarray
# np.array always copies an object
# np.asarray copies an object if necessary
def to_array(image: Image.Image) -> np.ndarray:
    array = np.array(image)
    return array