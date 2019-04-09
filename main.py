#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sys

import maze
import engine
import image
import enemy
import battle
import getch
import inventory

import constants

import random

# Handle input from the terminal
def process_input(command):
    # Convert the command to lowercase
    if (command.isupper()):
        command = command.lower()

    # Is it ctrl-C or escape? Exit.
    if command in ['\x1b','\x03']:
        sys.exit()

    # Quit
    if command in ('exit', 'quit'):
        sys.exit()

    # Map state
    elif constants.game_state['mode'] == 'main':
        if command == 'w':
            move_player (0, -1)
        elif command == 's':
            move_player (0, 1)
        elif command == 'a':
            move_player (-1, 0)
        elif command == 'd':
            move_player (1, 0)
        elif command in ['e','i']:
            constants.game_state['mode'] = 'bag'
            constants.game_state['return_mode'] = 'main'

    # Movement in battle mode
    elif constants.game_state['mode'] == 'battle':
        if command == 'w':
            battle.move_cursor(0)
        elif command == 's':
            battle.move_cursor(1)
        elif command == 'a':
            battle.move_cursor(2)
        elif command == 'd':
            battle.move_cursor(3)
        elif command == ' ':
            battle.select()

    # Bag inputs
    elif constants.game_state['mode'] == 'bag':
        if command == 'q':
            constants.game_state['mode'] = constants.game_state['return_mode'] 
            inventory.selected = 0
        if command == 'w':
            inventory.selected = max(inventory.selected - 1, 0)
        if command == 's':
            inventory.selected = min(inventory.selected + 1, len(inventory.loot_together) - 1)
        if command == ' ':
            inventory.select()

# Moves the player around the map
def move_player(x, y):
    global player_x
    global player_y

    if maze.maze[1 + player_y + y][2*(1 + player_x + x)] != constants.FULL_CELL:
        player_x += x
        player_y += y

def run(key):
    global player_x
    global player_y

    # Handle the new keypress
    process_input(key)

    # Draw the title screen
    if constants.game_state['mode'] == 'menu':
        engine.draw_buf(title.data, (0, 0))
        constants.game_state['mode'] = 'intro'

    # Play the intro cutscene
    elif constants.game_state['mode'] == 'intro':
        # Draw a text box
        engine.draw_text_box(0, 0, 79, 4,
            text = "       -- W E L C O M E   T O   P O R K   A N D   A D V E N T U R E! --       \n"
                   "             wasd to move, space to select, e for inventory.                  \n"
                   "                         Press space to continue",
            fill = True,

            delay = 0.02
        )
        constants.game_state['mode'] = 'main'

    # Map movement
    elif constants.game_state['mode'] == 'main':
        # Draw Maps
        collision = enemy.check_collision((player_y,player_x))
        if type(collision) == int:
            engine.draw_buf(battlescreen.data)
            constants.game_state['mode'] = 'battle_transition'
            battle.start_battle(collision)
        else:
            engine.draw_enemies(enemy.enemies)
            engine.draw_buf(maze.maze, (0,1))
            engine.plot(constants.PLAYER_CHAR, (1 + player_y, 3 + 2 * player_x))
            enemy.move_enemies()

    # Disable input in first frame of battle
    elif constants.game_state['mode'] == 'battle_transition':
        battle.battle()
        constants.game_state['mode'] = 'battle'

    # Battle scene
    elif constants.game_state['mode'] == 'battle':
        battle.battle()

    # Screen when you win the battle
    elif constants.game_state['mode'] == 'win_screen':
        constants.game_state['mode'] = 'main'

        # Won the floor!
        if len(enemy.enemies) == 0:
            # Reset everything
            constants.game_state['mode'] = 'next_floor'
            constants.game_state['level'] += 1
            maze.regen_maze((4,4))
            enemy.enemies = enemy.generate_enemies()
            player_x = 0
            player_y = 0

    # Levelup screen
    elif constants.game_state['mode'] == 'next_floor':
        engine.draw_buf(levelup.data)
        constants.game_state['mode'] = 'main'

    # You succ lol
    elif constants.game_state['mode'] == 'lose_screen':
        engine.draw_text_box(0,0,79,4, text= "                             B O O   Y O U   D I E D")

    # Don't run away boo
    elif constants.game_state['mode'] == 'run_screen':
        engine.draw_text_box(0,0,79,4, text= "                              ran away successfully!")
        constants.game_state['mode'] = 'main'

    # Bag state
    elif constants.game_state['mode'] == 'bag':
        inventory.draw_inventory()

    # Draw the screen to the terminal
    engine.draw()

# Images!
title = image.convert('images/title.txt')
battlescreen = image.convert('images/battlescreen.txt')
levelup = image.convert('images/levelup.txt')

player_x = 0
player_y = 0

if __name__ == '__main__':
    try:
        run(b' ')

        while (1):
            run(getch.getch())
    except KeyboardInterrupt:
        sys.exit()
