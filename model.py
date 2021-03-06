from random import randint

from funcCheck import is_hit
from game_variables import *
import arcade.key

DIR_STILL = 0
DIR_RIGHT = 2
DIR_LEFT = 4

DIR_OFFSETS = {DIR_STILL: (0, 0), DIR_RIGHT: (1, 0), DIR_LEFT: (-1, 0)}

MOVEMENT_SPEED = 5

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.directon = DIR_STILL
    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]

    def update(self, delta):
        self.move(self.directon)

class Monster:
    MONSTER_SPEED = 1
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.temp = 200
    def update(self,delta):
        self.y -= Monster.MONSTER_SPEED
        if self.y % 15 == 0:
            if self.x == self.temp:
                self.x = self.temp+50
            else:
                self.x = self.temp
        if self.y == 0:
            self.y = SCREEN_HEIGHT
            self.x = randint(50, 400)
            self.temp = self.x

    def hit(self, player):
        return is_hit(player.x, player.y, self.x, self.y)
    


class Bomb:
    BOMB_SPEED = 2

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0.2

    def up_speed(self):
        Bomb.BOMB_SPEED += self.vy    

    def update(self, delta):
        self.y -= Bomb.BOMB_SPEED
        if self.y < -20:
            self.y = SCREEN_HEIGHT
            self.x = randint(50, 400)
    def hit(self, player):
        return is_hit(player.x, player.y, self.x, self.y)


class Coin:
    COIN_SPEED = 1

    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.vy = 0.1

    def up_speed(self):
        Coin.COIN_SPEED += self.vy

    def is_position_negative(self):
        if self.y < 0:
            self.y = 0

    def update(self, delta):
        self.y -= Coin.COIN_SPEED
        if self.y < -20:
            self.y = SCREEN_HEIGHT
            self.x = randint(50, 400)

    def hit(self, player):
        return is_hit(player.x, player.y, self.x, self.y)

    def random_position(self):
        self.x = randint(50, 400)


class World:
    STATE_STOP = 1
    STATE_START = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player = Player(self, width // 2, height // 6)
        self.state = World.STATE_STOP
        self.coin = [
            Coin(self, width - 100, height),
            Coin(self, width - 200, height + 100),
            Coin(self, width - 250, height + 200),
            Coin(self, width - 300, height + 300),
            Coin(self, width - 200, height + 400),
        ]
        self.bomb = [Bomb(self, width // 4, height + 100),
                    Bomb(self, width // 2, height + 300),
                    Bomb(self, width // 6, height + 400)]
        self.monster = Monster(self,width//2,height + 100)
        self.score = 0
        self.level = 0
        self.level_bomb = 5
        self.level_monster = 2
        self.hp = 2
        self.st = False
        self.high_score_coin = 0

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score

    def get_level(self):
        return self.level

    def up_level(self):
        if self.get_score() % 5 == 0:
            self.level += 1
            for i in self.coin:
                i.up_speed()

    def start(self):
        self.state = World.STATE_START

    def freeze(self):
        self.state = World.STATE_STOP

    def is_start(self):
        return self.state == World.STATE_START
    
    def start_new_game(self):
        if self.st == True:
            Coin.COIN_SPEED = 1
            for i in self.coin:
                temp = randint(100, 400)
                i.y = SCREEN_HEIGHT+temp
            for i in self.bomb:
                temp_bomb = randint(100, 400)
                i.y = SCREEN_HEIGHT+temp_bomb
            self.monster.y = SCREEN_HEIGHT+100
            self.st = False

    def limit_screen(self, width):
        if self.player.x >= width:
            self.player.x = 0
        elif self.player.x <= 0:
            self.player.x = width

    def die(self):
        self.state = World.STATE_DEAD
        open_file = open("score.txt", "r")
        high_score = str(open_file.read())
        if int(high_score) < self.score:
            old_score = str(self.score)
            write_new_score = open("score.txt", "w")
            write_new_score.write(old_score)
            write_new_score.close()
            self.high_score_coin = self.score
        else:
            self.high_score_coin = int(high_score)

    def is_dead(self):
        return self.state == World.STATE_DEAD
    
    def player_hit(self):
        if not self.hp < 0:
            self.hp -= 1

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.RIGHT:
            self.player.directon = DIR_RIGHT
        if key == arcade.key.LEFT:
            self.player.directon = DIR_LEFT

    def update(self, delta):
        if self.state in [World.STATE_STOP, World.STATE_DEAD]:
            return

        self.player.update(delta)
        
        if self.get_level() >= self.level_bomb:
            for j in self.bomb:
                j.update(delta)
                if j.hit(self.player):
                    j.y = SCREEN_HEIGHT
                    self.player_hit()
        for i in self.coin:
            i.update(delta)
            if i.hit(self.player):
                arcade.play_sound(SOUNDS['point'])
                self.increase_score()
                self.up_level()
                i.y = SCREEN_HEIGHT
                i.random_position()

        if self.get_level() >= self.level_monster:
            self.monster.update(delta)
            if self.monster.hit(self.player):
                self.monster.y = SCREEN_HEIGHT
                self.player_hit()
        self.start_new_game()


