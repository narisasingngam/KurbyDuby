from random import randint

from funcCheck import is_hit_coin
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

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

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

class Coin:
    COIN_SPEED = 1

    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y

    def update(self,delta):
        self.y -= Coin.COIN_SPEED
        if self.y == 0 :
            self.y = SCREEN_HEIGHT
            self.random_position()


    def hit(self,player):
        return is_hit_coin(player.x, player.y,self.x, self.y)
    def random_position(self):
        self.x = randint(50,400)



class World:
    STATE_FROZEN = 1
    STATE_START = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, width // 2, height // 6 )
        self.state = World.STATE_FROZEN
        self.coin = [Coin(self, width - 200, height),Coin(self, width - 200, height + 200)]
        self.score = 0

    def increase_score(self):
        self.score += 1

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

    def die(self):
        self.state = World.STATE_DEAD

    def is_dead(self):
        return self.state == World.STATE_DEAD

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT:
            self.player.directon = DIR_RIGHT
        if key == arcade.key.LEFT:
            self.player.directon = DIR_LEFT

    def update(self, delta):
        if self.state in [World.STATE_FROZEN,World.STATE_DEAD]:
            return

        self.player.update(delta)
        for i in self.coin:
            i.update(delta)
            if i.hit(self.player):
                self.die()
                self.increase_score()
