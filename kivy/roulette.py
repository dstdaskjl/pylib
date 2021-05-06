from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from canvas import CustomCanvas
from effect import RouletteEffect
from texture import CustomTexture

RGBA_DARK_GREY = [154/255, 155/255, 156/255, 1]
RGBA_GREY = [188/255, 190/255, 192/255, 1]
RGBA_WHITE = [1, 1, 1, 1]


class ButtonFloatLayout(ButtonBehavior, FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Roulette(CustomCanvas, CustomTexture):
    def __init__(self, x, y, width, height, count, items, on_press=lambda *_: None, on_release=lambda *_: None, **kwargs):
        super().__init__(**kwargs)
        self.x = x
        self.y = y
        self.width = width
        self.height= height
        self.count = count if count % 2 == 1 else count + 1
        self.items = items
        self.on_press = on_press
        self.on_release = on_release

    def create(self):
        roulette_layout = self._create_button_layout()
        roulette_layout.add_widget(self._create_roulette_shadow())
        roulette_layout.add_widget(self._create_roulette_scroll())
        roulette_layout.add_widget(self._create_roulette_gradient())
        self._add_items(roulette=roulette_layout.children[1].children[0])
        self._add_placeholders(roulette=roulette_layout.children[1].children[0])
        return roulette_layout

    def _add_items(self, roulette):
        for item in self.items:
            roulette.add_widget(
                Button(
                    text=str(item),
                    color=RGBA_WHITE,
                    font_size=self.height / 2,
                    text_size=(None, self.height),
                    size_hint=(1, None),
                    pos_hint={'x': 0, 'y': 0},
                    height=self.height,
                    padding=(0, self.height / 3),
                    background_color=(0, 0, 0, 0),
                    background_normal='',
                    background_down='',
                    on_press=self.on_press,
                    on_release=self.on_release
                )
            )

    def _add_placeholders(self, roulette):
        for i in [len(self.items) + i for i in range(self.count // 2)] + ([0] * (self.count // 2)):
            roulette.add_widget(
                widget=Button(
                    text='',
                    color=RGBA_WHITE,
                    font_size=self.height / 2,
                    height=self.height,
                    text_size=(None, self.height),
                    background_color=(0, 0, 0, 0),
                    background_normal='',
                    background_down='',
                ),
                index=i
            )

    def _create_button_layout(self):
        button_layout = ButtonFloatLayout(
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        button_layout.on_release = lambda *_: button_layout.parent.remove_widget(button_layout)
        return button_layout

    def _create_roulette_box(self):
        roulette_box = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
        )
        roulette_box.bind(children=lambda *_: self._update_minimum_height(boxlayout=roulette_box))
        return roulette_box

    def _create_roulette_gradient(self):
        roulette_gradient = Widget(
            size_hint=(None, None),
            size=(self.width, self.height * self.count),
            pos=(self.x, self.y - self.height * (self.count // 2))
        )
        self.gradient.create(widget=roulette_gradient, orientation='vertical', center=True, color=RGBA_GREY[:-1])
        self.line_rectangle.create(widget=roulette_gradient, color=RGBA_WHITE, width=1.5)
        return roulette_gradient

    def _create_roulette_scroll(self):
        roulette_scroll = ScrollView(
            size_hint=(None, None),
            size=(self.width, self.height * self.count),
            pos=(self.x, self.y - self.height * (self.count // 2)),
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=0,
            smooth_scroll_end=10,
            scroll_wheel_distance=200,
            effect_y=RouletteEffect(anchor=0, interval=self.height)
        )
        self.filled_rectangle.create(widget=roulette_scroll, color=RGBA_GREY)
        self.filled_rectangle.create(widget=roulette_scroll, color=RGBA_DARK_GREY, size=(self.width, self.height), pos=(self.x, self.y))
        self.filled_triangle.create(widget=roulette_scroll, color=RGBA_WHITE, points=(
            self.x + self.width * 0.8, self.y + self.height * 0.55, self.x + self.width * 0.85,
            self.y + self.height * 0.75, self.x + self.width * 0.9, self.y + self.height * 0.55
        ))
        self.filled_triangle.create(widget=roulette_scroll, color=RGBA_WHITE, points=(
            self.x + self.width * 0.8, self.y + self.height * 0.45, self.x + self.width * 0.85,
            self.y + self.height * 0.25, self.x + self.width * 0.9, self.y + self.height * 0.45
        ))
        roulette_scroll.add_widget(self._create_roulette_box())
        return roulette_scroll

    def _create_roulette_shadow(self):
        roulette_shadow = Widget(
            size_hint=(None, None),
            size=(self.width, self.height * self.count),
            pos=(self.x, self.y - self.height * (self.count // 2))
        )
        self.shadow.create(widget=roulette_shadow)
        return roulette_shadow

    def _update_minimum_height(self, boxlayout):
        boxlayout.minimum_height = sum(child.height for child in boxlayout.children)
        boxlayout.height = boxlayout.minimum_height
