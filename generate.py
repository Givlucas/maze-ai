import numpy as np
import random
import queue
from PIL import Image

def cardinals(pos):
    x, y = pos
    list = []
    list.append((x, y-2))
    list.append((x+2, y))
    list.append((x, y+2))
    list.append((x-2, y))
    return list


def connection(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    x = (x1+x2) // 2
    y = (y1+y2) // 2
    return (x, y)


def generate_maze(xsize, ysize):
    maze = np.full((xsize, ysize), 1)
    start = (random.randrange(xsize+1), random.randrange(ysize+1))
    walls = set()
    # Assign start of maze to be a passage (0)
    maze[start] = 0

    # add frontiers if walls, to the wall list
    frontiers = cardinals(start)
    for pos in frontiers:
        # Check if x is out of bounds
        if pos[0] >= 0 and pos[0] < xsize-1 and maze[pos] == 1:
            # Check if y is out of bounds:
            if pos[1] >= 0 and pos[1] < ysize-1:
                walls.add(pos)

    while len(walls) > 0:
        # Choose a random walls
        loc = random.choice(tuple(walls))
        walls.remove(loc)
        # check if this is the last wall
        # if so set to 3 so we know where the end of the maze is
        if not len(walls):
            end = loc
        maze[loc] = 0
        card = cardinals(loc)

        neighbors = set()
        for pos in card:
            # Check if x is out of bounds
            if pos[0] >= 0 and pos[0] < xsize-1:
                # Check if y is out of bounds:
                if pos[1] >= 0 and pos[1] < ysize-1:
                    if maze[pos] == 0:
                        neighbors.add(pos)

        rand_neighbor = random.choice(tuple(neighbors))
        neighbors.remove(rand_neighbor)
        middle = connection(loc, rand_neighbor)
        maze[middle] = 0
        for pos in card:
            # Check if x is out of bounds
            if pos[0] >= 0 and pos[0] < xsize-1:
                # Check if y is out of bounds:
                if pos[1] >= 0 and pos[1] < ysize-1:
                    if maze[pos] == 1:
                        walls.add(pos)
    # label start and end of maze so that
    # we know where to start and end when we solve
    maze[start] = 2
    maze[end] = 3
    return (maze, start, end)


def solve_maze(maze, start, end):
    '''
       Takes a np array and solves a maze
    '''
    # algo:
    # 1) find the start of the maze (2) and end (3)
    # 2) append start to queue and set its distance to -1
    # 3) start loop until queue is empty
    # 4) when an element is popped add all its neighbors to the qeueue
    #    and decrease the distance by 1
    # 5) repeat untill queue empty
    # 6) start at end and go to next highest pixel to find shortest path
    #    highlighting the original maze at (x,y) red untill start is found


if __name__ == '__main__':
    xsize = 100
    ysize = 100
    maze, start, end = generate_maze(xsize, ysize)
    print(maze)
    img = Image.new('RGB', (xsize, ysize), color='black')
    for x in range(xsize):
        for y in range(ysize):
            if maze[x][y] == 0:
                img.putpixel((x, y), (255, 255, 255))
            elif maze[x][y] == 2:
                img.putpixel((x, y), (255, 0, 0))
            elif maze[x][y] == 3:
                img.putpixel((x, y), (0, 255, 0))
    # save the image as a bitmap file
    img.save('mazes/bitmap.bmp')