import time
from pyglet.window import mouse

from important_variables import *
import pyglet
from pyglet import window, clock

window = pyglet.window.Window(screen_length, screen_height, title)
mouse_buttons = pyglet.window.mouse.MouseStateHandler()

window.push_handlers(mouse_buttons)
mouse_position = [0, 0]

class Data:
    batch = pyglet.graphics.Batch()
    background_filler = pyglet.shapes.Rectangle(0, 0, screen_length, screen_height, color=background_color, batch=batch)
    should_pause = False
    time_needed = 0
    pause_start = 0

shapes = []

def get_top_edge_conversion(top_edge, height):
    return int(screen_height - top_edge - height)

def convert_to_int(*args):
    return_value = []

    for arg in args:
        return_value.append(int(arg))

    return return_value

def call_every_cycle(function):
    clock.schedule_interval(lambda unused: _call_every_cycle(function), 1.0 / 60.0)
    pyglet.app.run()

def _call_every_cycle(function):
    Data.batch.draw()

    if time.time() - Data.pause_start > Data.time_needed:
        Data.should_pause = False

    if not Data.should_pause:
        function()

def get_mouse_position():
    return mouse_position

@window.event
def on_mouse_motion(x, y, dx, dy):
    mouse_position[:] = [x, y]

def mouse_was_pressed():
    return mouse_buttons[pyglet.window.mouse.LEFT]

def clear_screen():
    Data.batch = pyglet.graphics.Batch()
    shapes[:] = []
    Data.background_filler = pyglet.shapes.Rectangle(0, 0, screen_length, screen_height, color=background_color, batch=Data.batch)

def draw_circle(left_edge, top_edge, length, height, color, outline_height):
    diameter = min(length, height)
    left_edge, top_edge = convert_to_int(left_edge, top_edge)

    radius = diameter // 2
    inner_circle_radius = radius - outline_height

    shapes.append(pyglet.shapes.Circle(left_edge + radius, top_edge + radius, radius, color=color, batch=Data.batch))
    shapes.append(pyglet.shapes.Circle(left_edge + radius, top_edge + radius, inner_circle_radius, color=background_color, batch=Data.batch))

def draw_line(start_x_coordinate, end_x_coordinate, start_y_coordinate, end_y_coordinate, color, line_height):
    start_x_coordinate, end_x_coordinate, start_y_coordinate, end_y_coordinate, line_height = convert_to_int(start_x_coordinate, end_x_coordinate, start_y_coordinate, end_y_coordinate, line_height)

    shapes.append(pyglet.shapes.Line(start_x_coordinate, start_y_coordinate, end_x_coordinate, end_y_coordinate, line_height, color=color, batch=Data.batch))

def update_display():
    pass

def pause_game(time_needed):
    Data.should_pause = True
    Data.time_needed = time_needed
    Data.pause_start = time.time()