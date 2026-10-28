import math
import time

from pico2d import *
from transitions import Machine


class Boy:
    IDLE_DURATION = 5
    SLEEP_Y = 70
    RUN_SPEED = 200
    RUN_FRAME_DURATION = 0.1
    SCREEN_WIDTH = 800
    WIDTH = 100

    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.direction = 1
        self.last_update_at = time.monotonic()
        self.run_frame_elapsed = 0
        self.image = load_image('animation_sheet.png')
        self.machine = Machine(
            model=self,
            states=['IDLE', 'RUN', 'SLEEP'],
            initial='IDLE',
            auto_transitions=False,
            transitions=[
                {'trigger': 'sleep', 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake', 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'run', 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
                {'trigger': 'stop', 'source': 'RUN', 'dest': 'IDLE'},
            ],
        )
        self.state_started_at = time.monotonic()

    def update(self):
        now = time.monotonic()
        delta_time = now - self.last_update_at
        self.last_update_at = now

        if self.state == 'IDLE':
            if now - self.state_started_at >= self.IDLE_DURATION:
                self.sleep()
                self.state_started_at = now
                return
            self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.x = min(
                max(self.x + self.direction * self.RUN_SPEED * delta_time, self.WIDTH / 2),
                self.SCREEN_WIDTH - self.WIDTH / 2,
            )
            self.run_frame_elapsed += delta_time
            if self.run_frame_elapsed >= self.RUN_FRAME_DURATION:
                self.frame = (self.frame + int(self.run_frame_elapsed / self.RUN_FRAME_DURATION)) % 8
                self.run_frame_elapsed %= self.RUN_FRAME_DURATION

    def handle_event(self, event):
        if (
            self.state == 'SLEEP'
            and event.type == SDL_KEYDOWN
            and event.key == SDLK_SPACE
        ):
            self.wake()
            self.state_started_at = time.monotonic()
        elif (
            self.state in ('IDLE', 'RUN', 'SLEEP')
            and event.type == SDL_KEYDOWN
            and event.key in (SDLK_LEFT, SDLK_RIGHT)
        ):
            direction = -1 if event.key == SDLK_LEFT else 1
            if self.state in ('IDLE', 'SLEEP'):
                self.direction = direction
                self.frame = 0
                self.run_frame_elapsed = 0
                self.run()
            elif self.direction != direction:
                self.direction = direction
                self.frame = 0
                self.run_frame_elapsed = 0
        elif (
            self.state == 'RUN'
            and event.type == SDL_KEYUP
            and event.key in (SDLK_LEFT, SDLK_RIGHT)
        ):
            self.stop()
            self.state_started_at = time.monotonic()
            self.frame = 0

    def draw(self):
        if self.state == 'IDLE':
            self.image.clip_draw(self.frame * 100, 300, 100, 100, self.x, self.y)
        elif self.state == 'RUN':
            row = 100 if self.direction == 1 else 0
            self.image.clip_draw(self.frame * 100, row, 100, 100, self.x, self.y)
        elif self.state == 'SLEEP':
            self.image.clip_composite_draw(
                0, 300, 100, 100, math.pi / 2, '', self.x, self.SLEEP_Y, 100, 100
            )
