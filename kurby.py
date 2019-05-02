import arcade

from model import World,Coin

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
    DELAY = 5
    temp_list=[]
    def __init__(self, width, height):
        super().__init__(width, height)

        self.background = arcade.load_texture("images/bgni.jpg")

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dot_sprite = ModelSprite('images/player.png', model=self.world.player)
        self.monster_sprite = MonsterSprite(model=self.world.monster)
        self.coin_sprite = [CoinSprite(model=self.world.coin[0]),CoinSprite(model=self.world.coin[1]),
                            CoinSprite(model=self.world.coin[2]),CoinSprite(model=self.world.coin[3]),
                            CoinSprite(model=self.world.coin[4])]
        self.bomb_sprite = [BombSprite(model=self.world.bomb[0]),BombSprite(model=self.world.bomb[1]),
                            BombSprite(model=self.world.bomb[2])]
        self.hp = [arcade.load_texture("images/pills.png"),arcade.load_texture("images/pills.png"),arcade.load_texture("images/pills.png")]
        self.num_hp = 2
        self.menus = {'gameover':arcade.load_texture("images/gameover.png"),
                      'play':arcade.load_texture("images/play.png")}
        self.count = 0
        self.temp_player = 1

    def setup(self):
        self.background = arcade.load_texture("images/bgni.jpg")
        self.hp = [arcade.load_texture("images/pills.png"),arcade.load_texture("images/pills.png"),arcade.load_texture("images/pills.png")]
        self.num_hp = 2
        self.world.level = 0
        self.world.score = 0
        self.world.hp = 2
        self.world.level_bomb = 5
        self.world.level_monster = 2
        self.monster_sprite.monster_sprite = arcade.Sprite('images/monster.png')
        self.dot_sprite = ModelSprite('images/player.png', model=self.world.player)
        
    def on_key_press(self, key, key_modifiers):
        if not self.world.is_start():
            self.world.start()
        self.world.on_key_press(key, key_modifiers)
        if self.world.level >= 3:
            if self.temp_player == 2 :
                self.temp_player = 1
            elif self.temp_player >= 1 :
                self.temp_player = 2
            self.dot_sprite = ModelSprite('images/kur'+str(self.temp_player)+'.png', model=self.world.player)

    def night_back(self):
        if self.world.level >= 5:
            self.background = arcade.load_texture("images/bg.jpg")
            self.monster_sprite.monster_sprite = arcade.Sprite('images/monster2.png')

    def update(self, delta):
        self.world.update(delta)
        self.world.limit_screen(SCREEN_WIDTH)
        self.night_back()

    def draw_background(self):
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
    def draw_detail(self):
        if self.world.level < 10 :
            color = arcade.color.BLACK
        else:
            color = arcade.color.WHITE

        arcade.draw_text('Score : '+str(self.world.score),
                         self.width - 80,
                         self.height - 30,
                         color,
                         12, )

        arcade.draw_text('Level : '+str(self.world.level),
                         self.width - 400,
                         self.height - 30,
                         color,
                         12, )
        arcade.draw_text('HP : ',
                         self.width - 400,
                         self.height - 60,
                         color,
                         12, )
        temp = 0
        if self.world.hp != self.num_hp:
            self.hp.pop()
            self.num_hp = self.world.hp

        for i in self.hp:
            arcade.draw_texture_rectangle(self.width - 360+temp, self.height - 53,10, 12,i)
            temp += 15

    def on_draw(self):
        arcade.start_render()
        # Draw the background texture
        self.draw_background()
        for i in self.coin_sprite:
            i.draw()
        self.dot_sprite.draw()
        self.draw_detail()
        for j in self.bomb_sprite:
            j.draw()
        self.monster_sprite.draw()


        if len(self.hp) == 0:
            self.world.die()
            texture = self.menus['gameover']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 + 50, texture.width, texture.height, texture, 0)
            texture = self.menus['play']
            arcade.draw_texture_rectangle(self.width//2, self.height//2 - 100, texture.width, texture.height, texture, 0)

    def on_mouse_press(self, x, y, button, modifiers):
        if len(self.hp) == 0:
            texture = self.menus['play']
            h = self.height//2 - 100
            w = self.width//2
            if w - texture.width//2 <= x <= w + texture.width//2:
                if h - texture.height//2 <= y <= h + texture.height//2:
                    self.world.st = True
                    self.setup()
                    self.world.start()

def main():
    window = KurbyWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == '__main__':
    main()
