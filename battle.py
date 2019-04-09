import enemy
import engine
from math import floor
import image
import constants 
import random
import inventory

from collections import Counter

# Loot you can find
# item name   |  item type | goodness
loottable_1 = [
(  'toothpick', 'weapon',  2),
(     'beanie',    'hat',  5),
('plastic bag',   'body',  5),
('single pant',   'legs',  5),
]
loottable_2 = [
(  'crab claw', 'weapon',  4),
('bike helmet',    'hat', 10),
( 'wood block',   'body', 10),
(     'pegleg',   'legs', 10),
]
loottable_3 = [
(      'fists', 'weapon',  8),
(   'hair net',    'hat', 20),
( 'Colorbond®',   'body', 20),
('thicc jeans',   'legs', 20),
]

foodtable_1 = [
(     'cookie', 'food', 7),
(   'doughnut', 'food', 8),
("for'n'tweny", 'food', 9),
(    'tendies', 'food', 5),
]
foodtable_2 = [
(        'egg', 'food',  8),
(   'jalapeno', 'food', 15),
(    'spinich', 'food', 12),
(        'BLT', 'food', 18),
]
foodtable_3 = [
( '¡cangrejo!', 'food', 20),
(       'cube', 'food', 24),
(      'bepis', 'food', 25),
( 'not butter', 'food', 28)
]

# Enemy you are currently fighting
current_battle = None

# Position of little arrow in fight menu ">"
cursor_pos = [3, 2]
selected = 0

# Player's HP
player_health = constants.START_MAX_HEALTH
player_max_health = constants.START_MAX_HEALTH

# Food and equipment
player_food = Counter()
player_equip = set({})

# Items the player is currently wearing
current_head = ('nothing', 'hat', 0)
current_body = ('nothing', 'body', 0)
current_legs = ('nothing', 'legs', 0)
current_weapon = ('nothing', 'weapon', 1)

# Crab image (O B A M A   I S   G O N E !!!)
crab = image.convert('images/crab.txt')

# Draw healthbar
def draw_bar(frac, size, pos):
    for i in range(size):
        engine.plot("▰▱"[floor(i/size - frac + 1)], (pos[0],pos[1] + i))

# Battle drawing and stuff
def battle():
    global cursor_pos

    # Draw the menu
    engine.draw_text_box(0,0,78,5, text=
        ' Your HP:                                Enemy HP:\n\n'

        '   FIGHT  |   BAG\n'
        '   KERMIT |   RUN')

    # Draw the crab and the little arrow UwU
    engine.draw_buf(crab.data, (6,0))
    engine.plot('>', tuple(cursor_pos))
    # Draw Enemy health bar
    draw_bar(current_battle['hp']/current_battle['max_hp'], 25, (1,52))
    # Draw Player health bar
    draw_bar(player_health/player_max_health, 25, (1,11))

# Called when you first start a battle
def start_battle(enemy_index):
    global current_battle
    current_battle = enemy.enemies.pop(enemy_index)

# Choose am item from the inventory
def choose_item():
    global player_equip
    global player_food
    equip_name = None
    food_name = None
    # Calculate drops
    table_choice = int(constants.game_state['level']/2)
    if table_choice == 0:
        loottable = loottable_1
        foodtable = foodtable_1
    elif table_choice == 1:
        loottable = loottable_2
        foodtable = foodtable_2
    else:
        loottable = loottable_3
        foodtable = foodtable_3

    # 50% chance of getting loot item
    if (random.randint(0,1)):
        random.shuffle(loottable)
        for item in loottable:
            if item not in player_equip:
                equip_name = item[0]
                player_equip.add(item)
                break

    # Always get food item
    item = random.choice(foodtable)
    player_food.update([item])
    food_name = item[0]

    return (food_name, equip_name)

# Move the cursor in the battle scene
def move_cursor(dp):
    global cursor_pos
    global selected

    if dp == 0 and cursor_pos[0] == 4:
        selected -= 1
        cursor_pos[0] = 3
    if dp == 1 and cursor_pos[0] == 3:
        selected += 1
        cursor_pos[0] = 4
    if dp == 3 and cursor_pos[1] == 2:
        selected += 2
        cursor_pos[1] = 13
    if dp == 2 and cursor_pos[1] == 13:
        selected -= 2
        cursor_pos[1] = 2

# Compute the player's maximum health from thier baseline + their armour
def compute_max_health():
    global player_max_health
    player_max_health = constants.START_MAX_HEALTH + current_head[2] + current_body[2] + current_legs[2]

# Bunch of behaviour triggered when you select a box.
def select():
    global current_battle
    global selected
    global cursor_pos
    global player_health
    global current_weapon
    # Fight
    if selected == 0:
        compute_max_health()
        current_battle['hp'] -= current_weapon[2]
        player_health -= current_battle['damage']
        # Player lost
        if player_health <= 0:
            constants.game_state['mode'] = 'lose_screen'

        # Player won
        elif (current_battle['hp'] <= 0):
            # Calculate drops
            items_gained = choose_item()

            if items_gained[1] == None:
                engine.draw_text_box(0,0,78,5,
                    text='                   You won the battle! You got a ' + items_gained[0] + '!')
            else:
                engine.draw_text_box(0,0,78,5,
                    text='       You won the battle! You got a ' + items_gained[0] + ' and a ' + items_gained[1] + '!')
            current_battle = None
            constants.game_state['mode'] = 'win_screen'
            selected = 0
            cursor_pos = [3, 2]
    # Open bag
    elif selected == 2:
        constants.game_state['mode'] = 'bag'
        constants.game_state['return_mode'] = 'battle'
    # Literally die
    elif selected == 1:
        constants.game_state['mode'] = 'lose_screen'
    # Try to run
    elif selected == 3:
        if random.randint(0,5) == 0:
            constants.game_state['mode'] = 'run_screen'
        else:
            player_health -= current_battle['damage']
            # Player lost
            if player_health <= 0:
                constants.game_state['mode'] = 'lose_screen'
