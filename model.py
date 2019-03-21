class Player:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y

        self.vy = 2

    def update(self, delta):
        self.y += self.vy
        # self.vy += 1


class World:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.player = Player(self, width // 2, height // 10)

    def update(self, delta):
        self.player.update(delta)
