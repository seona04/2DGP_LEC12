import math
import time

from pico2d import *
from transitions import Machine


class Boy:
    IDLE_DURATION = 5
    SLEEP_DURATION = 5
    SLEEP_Y = 80

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {'trigger': 'sleep', 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake', 'source': 'SLEEP', 'dest': 'IDLE'},
            ],
        )
        self.state_started_at = time.monotonic()

    def update(self):
        now = time.monotonic()

        if self.state == 'IDLE':
            if now - self.state_started_at >= self.IDLE_DURATION:
                self.sleep()
                self.state_started_at = now
                return
            self.frame = (self.frame + 1) % 8
        elif self.state == 'SLEEP':
            if now - self.state_started_at >= self.SLEEP_DURATION:
                self.wake()
                self.state_started_at = now

    def draw(self):
        if self.state == 'IDLE':
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        elif self.state == 'SLEEP':
            self.image.clip_composite_draw(
                0, 300, 100, 100, math.pi / 2, '', self.x, self.SLEEP_Y, 100, 100
            )
