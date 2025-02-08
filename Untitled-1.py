from pygame import *
from random import randint

class Explosion(Gamesprite):
    def __init__(self, x, y):
        super().__init__(explosion_images[0], x, y, 50, 50, 0)
        self.frames = [transform.scale(image.load(img), (50, 50)) for img in explosion_images]
        self.current_frame = 0
        self.last_update = time.get_ticks()