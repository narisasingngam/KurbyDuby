import arcade.key

DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0),
               DIR_RIGHT: (1, 0),
               DIR_LEFT: (-1, 0)}

MOVEMENT_SPEED = 4

class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

        self.directon = DIR_STILL

        self.vy = 2

    def move(self,direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]

    def update(self, delta):
        # self.y += self.vy
        self.move(self.directon)
        # self.vy += 1


class World:
    STATE_FROZEN = 1
    STATE_START = 2

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.player = Player(self, width // 2, height // 3)

        self.state = World.STATE_FROZEN

    def start(self):
        self.state = World.STATE_START

    def freeze(self):
        self.state = World.STATE_FROZEN

    def is_start(self):
        return self.state == World.STATE_START

    def limit_screen(self,width):
        if self.player.x >= width:
            self.player.x = width
        elif self.player.x <= 0:
            self.player.x = 0


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT:
            self.player.directon = DIR_RIGHT
        if key == arcade.key.LEFT:
            self.player.directon = DIR_LEFT

    def update(self, delta):
        if self.state == World.STATE_FROZEN:
            return
        self.player.update(delta)
