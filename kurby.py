import arcade

from model import World

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model", None)

        super().__init__(*args, **kwargs)

    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)

    def draw(self):
        self.sync_with_model()
        super().draw()

class CoinSprite:
    def __init__(self,model):
        self.model = model
        self.coin_sprite = arcade.Sprite('images/coin.png')

    def draw(self):
        self.coin_sprite.set_position(self.model.x, self.model.y)
        self.coin_sprite.draw()

class BombSprite:
    def __init__(self,model):
        self.model = model
        self.bomb_sprite = arcade.Sprite('images/bombs.png')
    
    def draw(self):
        self.bomb_sprite.set_position(self.model.x,self.model.y)
        self.bomb_sprite.draw()

class MonsterSprite:
    def __init__(self,model):
        self.model = model
        self.monster_sprite = arcade.Sprite('images/monster.png')
    def draw(self):
        self.monster_sprite.set_position(self.model.x,self.model.y)
        self.monster_sprite.draw()


class KurbyWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = arcade.load_texture("images/background.png")

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dot_sprite = ModelSprite('images/player.png', model=self.world.player)
        self.coin_sprite = [CoinSprite(model=self.world.coin[0]),CoinSprite(model=self.world.coin[1]),
                            CoinSprite(model=self.world.coin[2]),CoinSprite(model=self.world.coin[3]),
                            CoinSprite(model=self.world.coin[4])]
        self.bomb_sprite = [BombSprite(model=self.world.bomb[0]),BombSprite(model=self.world.bomb[1]),
                            BombSprite(model=self.world.bomb[2])]
        self.monster_sprite = MonsterSprite(model=self.world.monster)

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_start():
            self.world.start()
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        self.world.limit_screen(SCREEN_WIDTH)

    def draw_background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
    def draw_score(self):
        arcade.draw_text('Score : '+str(self.world.score),
                         self.width - 80,
                         self.height - 30,
                         arcade.color.BLACK,
                         12, )
    def draw_level(self):
        arcade.draw_text('Level : '+str(self.world.level),
                         self.width - 400,
                         self.height - 30,
                         arcade.color.BLACK,
                         12, )
    def draw_hp(self):
        arcade.draw_text('HP : '+str(self.world.hp)+'/100',
                         self.width - 400,
                         self.height - 60,
                         arcade.color.BLACK,
                         12, )


    def on_draw(self):
        arcade.start_render()
        # Draw the background texture
        self.draw_background()
        for i in self.coin_sprite:
            i.draw()
        self.dot_sprite.draw()
        # Draw the score
        self.draw_score()
        #Draw level
        self.draw_level()
        for j in self.bomb_sprite:
            j.draw()
        self.monster_sprite.draw()
        self.draw_hp()



def main():
    window = KurbyWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
