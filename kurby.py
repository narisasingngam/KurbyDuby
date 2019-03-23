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


class KurbyWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = arcade.load_texture("images/background.png")

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dot_sprite = ModelSprite('images/player.png', model=self.world.player)
        self.coin_sprite = [CoinSprite(model=self.world.coin[0]),CoinSprite(model=self.world.coin[1])]

    def on_key_press(self, key, key_modifiers):
        if not self.world.is_start():
            self.world.start()
        self.world.on_key_press(key, key_modifiers)

    def update(self, delta):
        self.world.update(delta)
        self.world.limit_screen(SCREEN_WIDTH)

    def on_draw(self):
        arcade.start_render()
        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        for i in self.coin_sprite:
            i.draw()
        self.dot_sprite.draw()
        # Draw the score
        arcade.draw_text(str(self.world.score),
            self.width - 60,
            self.height - 30,
            arcade.color.BLACK,
            20,)


def main():
    window = KurbyWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
