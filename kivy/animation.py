from kivy.animation import Animation as BaseAnim
from kivy.cache import Cache
from kivy.clock import Clock, mainthread


class Animation:
    def show(self, *args, duration=0.15, **kwargs):
        anim, anim_add = BaseAnim(opacity=1, duration=duration), BaseAnim(opacity=1, duration=duration)
        self.initialize(anim, anim_add, args, **kwargs)

    def hide(self, *args, duration=0.15, **kwargs):
        anim, anim_add = BaseAnim(opacity=0, duration=duration), BaseAnim(opacity=0, duration=duration)
        self.initialize(anim, anim_add, args, **kwargs)

    def blink(self, *args, duration=1.0, **kwargs):
        anim = BaseAnim(opacity=1, duration=duration) + BaseAnim(opacity=0, duration=duration)
        anim_add = BaseAnim(opacity=1, duration=duration) + BaseAnim(opacity=0, duration=duration)
        anim.repeat, anim_add.repeat = True, True
        self.initialize(anim, anim_add, args, **kwargs)

    def slide(self, *args, dest_pos, duration=0.15, **kwargs):
        anim, anim_add = BaseAnim(pos=dest_pos, duration=duration), BaseAnim(pos=dest_pos, duration=duration)
        self.initialize(anim, anim_add, args, **kwargs)

    def color(self, *args, color, duration=1.0, **kwargs):
        anim, anim_add = BaseAnim(color=color, duration=duration), BaseAnim(color=color, duration=duration)
        self.initialize(anim, anim_add, args, **kwargs)

    def play(self, *args, delay):
        for img in args:
            img.anim_delay = delay

    def stop(self, *args):
        for img in args:
            img.anim_delay = -1

    def cancel(self, *args):
        [BaseAnim.cancel_all(widget=widget) for widget in args]

    @mainthread
    def reset(self, *args):
        for img in args:
            if hasattr(img, '_coreimage'):
                if img._coreimage.image.textures == 1:
                    img.reload()
                else:
                    self.stop(img)
                    img._coreimage._anim_index = 0
                    img._coreimage._anim()
                    img._coreimage._anim_index = 0
            else:
                img.texture_update()

        Cache.remove('kv.image')
        Cache.remove('kv.texture')

    def schedule(self, callback, timeout=0):
        Clock.schedule_once(callback=lambda t: callback(), timeout=timeout)

    def interval(self, callback, timeout=0):
        Clock.schedule_interval(callback=lambda t: callback(), timeout=timeout)

    def initialize(self, *args, **kwargs):
        anim, anim_add, targets = args
        Bind(anim).all(
            on_start       =kwargs['on_start'   ] if 'on_start'    in kwargs else lambda: None,
            on_progress    =kwargs['on_progress'] if 'on_progress' in kwargs else lambda: None,
            on_complete    =kwargs['on_complete'] if 'on_complete' in kwargs else lambda: None,
            exp_progression=kwargs['progression'] if 'progression' in kwargs else 0
        )
        targets = list(targets)
        anim.start(widget=targets.pop(0))
        [anim_add.start(target) for target in targets]


class Bind:
    def __init__(self, anim):
        self.anim = anim

    def all(self, **kwargs):
        self.__on_start   (on_start   =kwargs['on_start'])
        self.__on_progress(on_progress=kwargs['on_progress'], expected_progression=kwargs['exp_progression'], flag=Flag())
        self.__on_complete(on_complete=kwargs['on_complete'])

    def __on_start(self, on_start):
        self.anim.bind(on_start=lambda animation, widget: on_start())

    def __on_progress(self, on_progress, expected_progression, flag):
        def trace_progress(progression):
            if flag.value and progression < expected_progression:
                flag.update()
            elif not flag.value and progression >= expected_progression:
                flag.update()
                return on_progress()

        if expected_progression != 0:
            self.anim.bind(
                on_progress=lambda animation, widget, progression: trace_progress(progression=progression)
            )

    def __on_complete(self, on_complete):
        self.anim.bind(on_complete=lambda animation, widget: on_complete())


class Flag:
    def __init__(self):
        self.value = False

    def update(self):
        self.value = not self.value
