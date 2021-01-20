import numpy as np
import sys
import os
import time

import constants

# We need this to print correctly to the screen
from  unicodedata import east_asian_width

# Nice little text box
def draw_text_box(x, y, w, h, text='', fill=False, delay=0):
    global screen

    # Fill with spaces first.
    if fill:
        screen = blit(screen, [[' '] * w for i in range(h)], (y,x))

    # Draw corners
    screen[y][x]     = '╔'
    screen[y][x+w]   = '╗'
    screen[y+h][x]   = '╚'
    screen[y+h][x+w] = '╝'

    # Draw edges
    for i in range(w - 1):
        screen[y][x+i+1]   = '═'
        screen[y+h][x+i+1] = '═'
    for i in range(h - 1):
        screen[y+i+1][x]   = '║'
        screen[y+i+1][x+w] = '║'

    # Draw text (if any) with delay (if any)
    if text != '':
        if delay:
            for i,line in enumerate(text.split('\n')):
                for j,char in enumerate(line):
                    screen[y + 1 + i][x + 1 + j] = char
                    if char != ' ':
                        draw(do_flush=False)
                        if char in '.,!?:':
                            time.sleep(delay*6)
                        else:
                            time.sleep(delay)
        else:
            for i,line in enumerate(text.split('\n')):
                for j,char in enumerate(line):
                    screen[y + 1 + i][x + 1 + j] = char

# Text without the textbox
def draw_text(x,y,text):
    for i,line in enumerate(text.split('\n')):
        for j,char in enumerate(line):
            screen[y + i][x + j] = char

# Clear the screen
def flush():
    global screen
    screen = [[' '] * constants.WIDTH for i in range(constants.HEIGHT)]

# Pretty self descriptive, returns column major tuple
def get_terminal_size():
    try:
        terminal_size = os.get_terminal_size(0)
    except OSError:
        terminal_size = os.get_terminal_size(1)

    return tuple(terminal_size)

# Draw the buffer to the screen NO CMD!! >:(
def draw(do_flush=True):
    # Draw the current frame to the screen.
    global old_dim
    global frame

    get_terminal_size()

    # If the dimensions have changed
    if old_dim != terminal_size:
        # Clear the screen
        sys.stdout.write("\x1B[2J")

    old_dim = terminal_size

    # Turn screen data into a string
    output = ''

    for i in range(constants.HEIGHT):
        j = 0
        while j < constants.WIDTH:
            output += screen[i][j]
            if east_asian_width(screen[i][j]) in 'FW':
                j += 1
            j += 1
        output += '\n'
    # Print the frame
    sys.stdout.write("\x1b7\x1b[0;0f%s\x1b8" % output)

    # clear input box
    sys.stdout.write("\x1b7\x1b[24;0f"+ ' '*terminal_size[0] + "\x1b8")

    # Move cursor
    sys.stdout.write("\033[24;0H")

    # Flush the screen if the flush flag is on
    if do_flush: flush()

    frame += 1

def plot(c, offsets=(0,0)):
    """
    Plot a char (c) to offset (y,x)
    """
    global screen
    screen[offsets[0]][offsets[1]] = c

def blit(a, b, offsets=(0,0), transparent_char='α'):
    """
    a: an array object or a tuple is as_shape is True
    b: an array object or a tuple is as_shape is True
    offsets: a sequence of offsetsWn

    return: a multidimensional slice for <a> followed by a multidimensional slice for <b>
    """

    # Retrieve and check the array shapes and offset
    a, b = np.array(a, copy=False), np.array(b, copy=False)
    a_shape, b_shape = a.shape, b.shape

    n = min(len(a_shape), len(b_shape))
    if n == 0:
        raise ValueError("Cannot overlap with an empty array")
    offsets = tuple(offsets) + (0,) * (n - len(offsets))
    if len(offsets) > n:
        raise ValueError("Offset has more elements than either number of dimensions of the arrays")

    # Compute the slices
    a_slices, b_slices = [], []
    for i, (a_size, b_size, offset) in enumerate(zip(a_shape, b_shape, offsets)):
        a_min = max(0, offset)
        a_max = min(a_size, max(b_size + offset, 0))
        b_min = max(0, -offset)
        b_max = min(b_size, max(a_size - offset, 0))
        a_slices.append((a_min, a_max))
        b_slices.append((b_min, b_max))

    a_slice, b_slice = tuple(a_slices), tuple(b_slices)

    # Copy the slices with transparency
    for y in range(b_slice[0][0], b_slice[0][1]):
        for x in range(b_slice[1][0], b_slice[1][1]):
            if b[y][x] != transparent_char:
                a[y + a_slice[0][0]][x + a_slice[1][0]] = b[y][x]
    return a

def draw_buf(buf, offsets=(0,0), transparent_char='α'):
    # Draw an image to the screen (wrapper for blit)
    global screen
    screen = blit(screen,buf,offsets,transparent_char)

def draw_enemies(enemies):
    # Draw the enemies on the map
    global screen

    for i in enemies:
        plot(constants.ENEMY_CHAR,(i['pos'][0],i['pos'][1]))

terminal_size = get_terminal_size()
old_dim = (0,0)
# Define screen
screen = np.asarray([[' '] * constants.WIDTH for i in range(constants.HEIGHT)])
frame = 0
