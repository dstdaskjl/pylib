from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle


class CustomCanvas:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gradient = _Gradient()
        self.dynamic_filled_rectangle = _DynamicFilledRectangle()
        self.filled_circle = _FilledCircle()
        self.filled_rectangle = _FilledRectangle()
        self.filled_triangle = _FilledTriangle()
        self.line_rectangle = _LineRectangle()
        self.line_points = _LinePoints()


class _Gradient:
    def create(self, widget, orientation='horizontal', center=False, reverse=False, color=(1,1,1)):
        with widget.canvas.before:
            size = int(widget.width) if orientation == 'horizontal' else int(widget.height)
            with widget.canvas.before:
                for i in range(size):
                    Color(*color, i/size)
                    if orientation == 'horizontal':
                        if center:
                            if i % 2 == 0:
                                points = (widget.x + (widget.width / 2) + int(i / 2), widget.y, widget.x + (widget.width / 2) + int(i / 2), widget.y + widget.height)
                            else:
                                points = (widget.x + (widget.width / 2) - int(i / 2), widget.y, widget.x + (widget.width / 2) - int(i / 2), widget.y + widget.height)
                        elif reverse:
                            points = (widget.x + size - i, widget.y, widget.x + size - i, widget.y + widget.height)
                        else:
                            points = (widget.x + i, widget.y, widget.x + i, widget.y + widget.height)
                    else:
                        if center:
                            if i % 2 == 0:
                                points = (widget.x, widget.y + (widget.height / 2) + int(i / 2), widget.x + widget.width, widget.y + (widget.height / 2) + int(i / 2))
                            else:
                                points = (widget.x, widget.y + (widget.height / 2) - int(i / 2), widget.x + widget.width, widget.y + (widget.height / 2) - int(i / 2))
                        elif reverse:
                            points = (widget.x, widget.y + size - i, widget.x + widget.width, widget.y + size - i)
                        else:
                            points = (widget.x, widget.y + i, widget.x + widget.width, widget.y + i)
                    Line(width=1, points=points)


class _DynamicFilledRectangle:
    def create(self, widget, color, factors, z='before'):
        with widget.canvas.before if z=='before' else widget.canvas.after:
            Color(rgba=color)
            rectangle = Rectangle(
                size=(widget.size[0] / factors[2], widget.size[1] / factors[3]),
                pos=(widget.pos[0] + widget.size[0] / factors[0], widget.pos[1] + widget.size[1] / factors[1])
            )
            bound_func = lambda *args: self._update(source=widget, target=rectangle, factors=factors)
            widget.bind(size=bound_func, pos=bound_func)

    def _update(self, source, target, factors):
        x_factor, y_factor, width_factor, height_factor = factors
        target.size = source.size[0] / width_factor, source.size[1] / height_factor
        target.pos = source.pos[0] + source.size[0] / x_factor, source.pos[1] + source.size[1] / y_factor


class _FilledCircle:
    def create(self, widget, color, diameter, z='before'):
        with widget.canvas.before if z=='before' else widget.canvas.after:
            Color(rgba=color)
            ellipse = Ellipse(size=(widget.width, widget.width) if diameter == 'width' else (widget.height, widget.height), pos=widget.pos)
            bound_func = lambda *args: self._update(source=widget, target=ellipse, diameter=diameter)
            widget.bind(size=bound_func, pos=bound_func)

    def _update(self, source, target, diameter):
        size = (source.width, source.width) if diameter == 'width' else (source.height, source.height)
        target.size = size
        target.pos = source.pos


class _FilledRectangle:
    def create(self, widget, color, size=None, pos=None, z='before'):
        with widget.canvas.before if z=='before' else widget.canvas.after:
            Color(rgba=color)
            rectangle = Rectangle(size=size if size else widget.size, pos=pos if pos else widget.pos)
            if not size and not pos:
                bound_func = lambda *args: self._update(source=widget, target=rectangle)
                widget.bind(size=bound_func, pos=bound_func)

    def _update(self, source, target):
        target.size = source.size
        target.pos = source.pos


class _FilledTriangle:
    def create(self, widget, color, size_hint=(1, 1), pos_hint=(0, 0), flip=False, points=None, z='before'):
        with widget.canvas.before if z=='before' else widget.canvas.after:
            Color(rgba=color)
            triangle = Triangle(points=points if points else (0, 0, 0, 0, 0, 0))
            if not points:
                bound_func = lambda *args: self._update(
                    source=widget, target=triangle, size_hint=size_hint, pos_hint=pos_hint, flip=flip
                )
                widget.bind(size=bound_func, pos=bound_func)

    def _update(self, source, target, size_hint, pos_hint, flip):
        x, y = source.x + source.width * pos_hint[0], source.y + source.height * pos_hint[1]
        width, height = source.width * size_hint[0], source.height * size_hint[1]

        left = (x, y)
        mid = (x + (width / 2), y - height) if flip else (x + (width / 2), y + height)
        right = (x + width, y)
        target.points = (*left, *mid, *right)


class _LineRectangle:
    def create(self, widget, color, width, size=None, pos=None, z='before'):
        with widget.canvas.before if z=='before' else widget.canvas.after:
            Color(rgba=color)
            rect_pos = pos if pos else widget.pos
            rect_size = size if size else widget.size
            rectangle = Line(width=width, rectangle=(*rect_pos, *rect_size))
            if not size and not pos:
                bound_func = lambda *args: self._update(source=widget, target=rectangle)
                widget.bind(size= bound_func, pos=bound_func)

    def _update(self, source, target):
        target.rectangle = *source.pos, *source.size


class _LinePoints:
    def create(self, widget, color, width, points=None, z='before'):
        with widget.canvas.before if z=='before' else widget.canvas.after:
            Color(rgba=color)
            line = Line(width=width, points=points if points else (0, 0, 0, 0))
            if not points:
                bound_func = lambda *args: self._update(source=widget, target=line)
                widget.bind(size=bound_func, pos=bound_func)

    def _update(self, source, target):
        target.points = source.x, source.y + source.height / 2, source.x + source.width, source.y + source.height / 2
