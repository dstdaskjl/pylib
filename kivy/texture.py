import cv2

from kivy.core.image import Texture


class Background:
    def apply(self, *args):
        for widget in args:
            self._create(widget)
            self._update(widget)

    def _create(self, widget):
        x, y, width, height = int(widget.x), int(widget.y), int(widget.width), int(widget.height)
        bg = cv2.imread(BACKGROUND_IMAGE, cv2.IMREAD_UNCHANGED)
        flipped_bg = cv2.flip(bg, 0)
        cropped_bg = flipped_bg[y: y + height, x: x + width]
        texture = Texture.create(size=(cropped_bg.shape[1], cropped_bg.shape[0]), colorfmt='rgba')
        texture.blit_buffer(cropped_bg.tostring(), colorfmt='rgba', bufferfmt='ubyte')
        widget.texture = texture
        widget.texture.mag_filter = 'nearest'

    def _update(self, widget):
        widget.texture = ''
        func = lambda *args: self._create(widget=args[0])
        widget.bind(size=func, pos=func)
