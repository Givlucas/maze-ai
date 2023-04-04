import numpy as np
import random
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
        # print(walls)
        # print(loc)
        # print(maze)
    return maze


if __name__ == '__main__':
    xsize = 100
    ysize = 100
    maze = generate_maze(xsize, ysize)
    print(maze)
    img = Image.new('1', (xsize, ysize), color='black')
    for x in range(xsize):
        for y in range(ysize):
            if maze[x][y] == 0:
                img.putpixel((x, y), 1)
    # save the image as a bitmap file
    img.save('bitmap.bmp')