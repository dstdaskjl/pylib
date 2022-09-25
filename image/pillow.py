import numpy as np
from PIL import Image, ImageEnhance
from typing import Union


#  (0,0) starts from the top-left corner

#  https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
def convert(src: str, dst: str, mode: str):
    image = Image.open(src).convert(mode=mode)
    image.save(dst)

def crop(src: str, dst: str, top_left: tuple, bottom_right: tuple) -> None:
    image = Image.open(src).crop(*top_left, *bottom_right)
    image.save(dst)

def flip_left_right(src: str, dst: str) -> None:
    image = Image.open(src).transpose(method=Image.FLIP_LEFT_RIGHT)
    image.save(dst)

def flip_top_bottom(src: str, dst: str) -> None:
    image = Image.open(src).transpose(method=Image.FLIP_TOP_BOTTOM)
    image.save(dst)

def from_array(array: np.ndarray, mode=None) -> Image.Image:
    return Image.fromarray(array, mode)

def get_colors(src: str) -> list:
    return Image.open(src).getcolors()

def get_pixel(src: str, coord: tuple) -> Union[int, tuple]:
    return Image.open(src).getpixel(xy=coord)

def enhance(src: str, dst: str, factor: float) -> None:
    image = Image.open(src)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(factor=factor)
    image.save(dst)

def make_square(src: str, dst:str, size=0, fill_color=(0, 0, 0)):
    image = Image.open(src)
    x, y = image.size
    if not size:
        size = max(x, y)
    new_im = Image.new('RGB', (size, size), fill_color)
    new_im.paste(image, (int((size - x) / 2), int((size - y) / 2)))
    return new_im.save(dst)

def resize(src: str, dst: str, size: tuple, resample=Image.ANTIALIAS) -> None:
    image = Image.open(src).resize(size=size, resample=resample)
    image.save(dst)

def rotate(src: str, dst: str, angle: float, resample=Image.ANTIALIAS, center=None) -> None:
    image = Image.open(src).rotate(angle=angle, resample=resample, center=center)
    image.save(dst)

def to_array(src: str) -> np.ndarray:
    image = Image.open(src)
    array = np.array(image)
    return array
