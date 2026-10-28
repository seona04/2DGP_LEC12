from pico2d import *
import random


# Game object class here
from pico2d import load_image
import boy
import grass

def handle_events():
    global running, player

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            else:
                player.handle_event(event)
        elif event.type == SDL_KEYUP:
            player.handle_event(event)


def reset_world():
    global world, player

    world = []

    grass_object = grass.Grass()
    world.append(grass_object)

    player = boy.Boy()
    world.append(player)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
