import constants
import random
import numpy as np

def generate_maze(width, height):
    '''
    Depth first search algorithm:
    1.  Make the initial cell the current cell and mark it as visited
    2.  While there are unvisited cells
        1.  If the current cell has any neighbours which have not been visited
            1.  Choose randomly one of the unvisited neighbours
            2.  Push the current cell to the stack
            3.  Remove the wall between the current cell and the chosen cell
            4.  Make the chosen cell the current cell and mark it as visited
        2.  Else if stack is not empty
            1.  Pop a cell from the stack
            2.  Make it the current cell
    '''

    if width%2 and height%2 == 0:
        raise ValueError('Width and Height must be odd numbers.')

    maze = [[constants.FULL_CELL] * width for i in range(height)]
    stack = []

    # Pick starting position
    row = random.randint(0, int((height-2)/2)) * 2 + 1
    col = random.randint(0, int((width-2)/2)) * 2 + 1

    maze[row][col] = constants.EMPTY_CELL

    directions = [np.array([-1,0]), np.array([1,0]), np.array([0,-1]), np.array([0,1])]

    while (1):
        for choice in random.sample(directions, len(directions)):
            choice_pos = choice*2 + np.array([row, col])
            if choice_pos[0] < 0 or choice_pos[1] < 0 or choice_pos[0] >= height or choice_pos[1] >= width:
                continue
            elif maze[choice_pos[0]][choice_pos[1]] == constants.EMPTY_CELL:
                continue
            else:
                path_pos = choice + np.array([row, col])
                maze[choice_pos[0]][choice_pos[1]] = constants.EMPTY_CELL
                maze[path_pos[0]][path_pos[1]] = constants.EMPTY_CELL
                stack.append((row,col))
                row = choice_pos[0]
                col = choice_pos[1]
                break
        else:
            if len(stack) != 0:
                row,col = stack.pop()
            else:
                # Finish the algorithm
                break

    maze_scaled = [[None] * (width * 2) for i in range(height)]

    for i in range(height):
        for j in range(width):
            maze_scaled[i][(2*j)] = maze[i][j]
            maze_scaled[i][(2*j)+1] = maze[i][j]

    return maze_scaled


size = (13,9)

# Regenerate the maze (with change in maze size)
def regen_maze(delta_size):
    global maze
    global size

    size = (size[0] + delta_size[0], size[1] + delta_size[1])
    size = (min(size[0],39),min(size[1],23))

    # Create the maze
    maze = generate_maze(size[0], size[1])

regen_maze((0,0))
