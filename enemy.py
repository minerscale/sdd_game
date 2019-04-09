import random
import maze

import constants

# Randomly move the enemies on the screen sometimes
def move_enemies():
    enemy_pos = get_enemy_pos()

    for ind in range(len(enemies)):
        if random.randint(0,5) == 0:
            a = random.randint(0,1)*2 - 1
            b = random.randint(0,1)
            if b:
                x = a
                y = 0
            else:
                x = 0
                y = a
            if maze.maze[enemies[ind]['pos'][0] + y][enemies[ind]['pos'][1] + 2*x] != constants.FULL_CELL:
                if (enemies[ind]['pos'][0] + y, enemies[ind]['pos'][1] + 2*x) not in enemy_pos:
                    enemies[ind]['pos'] = (enemies[ind]['pos'][0] + y, enemies[ind]['pos'][1] + 2*x)
                    enemy_pos[ind] = enemies[ind]['pos']

# For collision detection
def get_enemy_pos():
    enemy_pos = []
    for i in enemies:
        enemy_pos.append(i['pos'])

    return enemy_pos

# Check if the player and an enemy is colliding, if so, collide with it
def check_collision(player_pos):
    enemy_pos = get_enemy_pos()

    try:
        ret = enemy_pos.index((1 + player_pos[0], 3 + 2 * player_pos[1]))
    except ValueError:
        ret = None
    return ret

# Generate enemies with damage and health and put them in the maze.
def generate_enemies():
    total = int((maze.size[0]/6)**2)
    ret = []
    for i in range(total):
        while True:
            enemy_x = random.randint(1,maze.size[0]-1)
            enemy_y = random.randint(1,maze.size[1]-1)

            if (maze.maze[enemy_y][enemy_x*2] == constants.EMPTY_CELL and enemy_x + enemy_y >= 4 and
                ((enemy_y,enemy_x*2 + 1) not in [j['pos'] for j in ret])):

                max_hp = random.randint(5,8)*(constants.game_state['level'] + 2)/6.0 + 3
                ret.append({
                    'pos': (enemy_y,enemy_x*2 + 1),
                    'hp': max_hp,
                    'max_hp': max_hp,
                    'damage': int((random.randint(12,18)/16.0)*(constants.game_state['level'] + 2))
                    })
                break
    return ret

enemies = generate_enemies()
