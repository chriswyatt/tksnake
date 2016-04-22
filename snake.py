from tkinter.ttk import *
from tkinter import *
import math
import random

GRID_WIDTH = 20
GRID_HEIGHT = 20
BLOCK_DIAM = 8
BLOCK_PAD = 2
UPDATE_INTERVAL = 100

def get_opposite_direction(rad):
    rad += math.pi
    if rad >= 0:  
        return rad % (2 * math.pi)
    elif rad < 0:
        return rad % (-2 * math.pi)

class Block(object):
    def __init__(self, x, y):
        self.point = (x, y)

    def __repr__(self):
        return str(self.point)

class GameObject(object):
    def __init__(self):
        self.blocks = []

class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.direction = 0
        self.direction_queue = []
        self.grow_count = 0

    def grow(self, count):
        self.grow_count += count

    def update(self, ):
        previous_points = [block.point for block in self.blocks]

        new_tail = None
        if self.grow_count > 0:
            tail_point = previous_points[len(previous_points) - 1]
            new_tail = Block(tail_point[0], tail_point[1])

        if(self.direction_queue):
            self.direction = self.direction_queue.pop(0)

        head = self.blocks[0]
        head.point = (
            head.point[0] + round(math.cos(self.direction)),
            head.point[1] + round(math.sin(self.direction)) * -1
        )

        for i, block in enumerate(self.blocks[1:]):
            block.point = previous_points[i]

        if new_tail:
            self.blocks.append(new_tail)
            self.grow_count -= 1

class Food(GameObject):
    pass

player_list = []
food_list = []

def create_food():
    global player_list
    global food_list

    food = Food()
    point = None
    # Will get stuck in loop if snake fills screen
    while point is None or point in [block.point for block in player_list[0].blocks]:
        point = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    food.blocks.append(Block(point[0], point[1]))
    food_list.append(food)

def init():
   global player_list
   global food_list

   player_list = []
   food_list = []

   player = Snake()
   player.blocks.extend([Block(6, 5), Block(5, 5)])
   player_list.append(player)

   create_food()

init()

class App:
    def __init__(self, master):
        self.canvas = Canvas(master, width=200, height=200)
        self.canvas.pack()

        [master.bind(key, self.on_direction_key_press) for key in ["<Up>", "<Right>", "<Down>", "<Left>"]]

        self.update()

    def on_direction_key_press(self, e):
        directions = {
            'Right': 0,
            'Up': math.pi / 2,
            'Left': math.pi,
            'Down': 3 * math.pi / 2
        }
        if player_list[0].direction_queue:
            last_direction_queued = player_list[0].direction_queue[len(player_list[0].direction_queue) - 1]
        else:
            last_direction_queued = player_list[0].direction
        if(directions[e.keysym] != get_opposite_direction(last_direction_queued)
           and directions[e.keysym] != last_direction_queued):
            if len(player_list[0].direction_queue) > 1:
                player_list[0].direction_queue = []
            player_list[0].direction_queue.append(directions[e.keysym])

    def update(self):
        global player_list
        global food_list

        self.canvas.delete(ALL)
        player_list[0].update()

        if(any([player_list[0].blocks[0].point == block.point for block in player_list[0].blocks[1:]])
           or player_list[0].blocks[0].point[0] not in range(0, GRID_WIDTH)
           or player_list[0].blocks[0].point[1] not in range(0, GRID_HEIGHT)):
            init()

        if not food_list or player_list[0].blocks[0].point == food_list[0].blocks[0].point:
            food_list = []
            create_food()
            player_list[0].grow(1)

        blocks = []
        blocks.extend(player_list[0].blocks)
        blocks.extend(food_list[0].blocks)

        for block in blocks:
            x = block.point[0] * (BLOCK_PAD + BLOCK_DIAM)
            y = block.point[1] * (BLOCK_PAD + BLOCK_DIAM)
            self.canvas.create_rectangle(x, y, x + BLOCK_DIAM, y + BLOCK_DIAM)

        self.canvas.after(UPDATE_INTERVAL, self.update)

root = Tk()

app = App(root)

root.mainloop()
