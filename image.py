import numpy as np
from PIL import Image as Im
from typing import Union


#  (0,0) starts from the top-left corner
class Image:
    #  https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
    def convert(self, src: str, dst: str, mode: str):
        image = Im.open(src).convert(mode=mode)
        image.save(dst)

    def crop(self, src: str, dst: str, top_left: tuple, bottom_right: tuple) -> None:
        image = Im.open(src).crop(*top_left, *bottom_right)
        image.save(dst)

    def flip_left_right(self, src: str, dst: str) -> None:
        image = Im.open(src).transpose(method=Im.FLIP_LEFT_RIGHT)
        image.save(dst)

    def flip_top_bottom(self, src: str, dst: str) -> None:
        image = Im.open(src).transpose(method=Im.FLIP_TOP_BOTTOM)
        image.save(dst)

    def from_array(self, array: np.ndarray, mode=None) -> Im.Image:
        return Im.fromarray(array, mode)

    def get_colors(self, src: str) -> list:
        return Im.open(src).getcolors()

    def get_pixel(self, src: str, coord: tuple) -> Union[int, tuple]:
        return Im.open(src).getpixel(xy=coord)

    def make_square(self, src: str, dst:str, size=0, fill_color=(0, 0, 0)):
        image = Im.open(src)
        x, y = image.size
        if not size:
            size = max(x, y)
        new_im = Im.new('RGB', (size, size), fill_color)
        new_im.paste(image, (int((size - x) / 2), int((size - y) / 2)))
        return new_im.save(dst)

    def resize(self, src: str, dst: str, size: tuple, resample=Im.ANTIALIAS) -> None:
        image = Im.open(src).resize(size=size, resample=resample)
        image.save(dst)

    def rotate(self, src: str, dst: str, angle: float, resample=Im.ANTIALIAS, center=None) -> None:
        image = Im.open(src).rotate(angle=angle, resample=resample, center=center)
        image.save(dst)

    def to_array(self, src: str) -> np.ndarray:
        image = Im.open(src)
        array = np.array(image)
        return array
