import arcade
import threading
from structs.Player import PlayerData


class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(800, 600, "捡金币")

        arcade.set_background_color(arcade.color.BLUE)

        self.player = arcade.Sprite("resources/me.png", 0.5)

        self.player.center_x = 400

        self.player.center_y = 300
        self.player.data = PlayerData(1, 100)

        self.coin = arcade.Sprite("resources/coin.png", 0.25)

        self.coin.center_x = 100

        self.coin.center_y = 100

        self.coin.data = PlayerData(1, 50)

        self.result = "Gaming..."

    def on_draw(self):
        arcade.start_render()

        self.coin.draw()

        self.player.draw()

        arcade.draw_text(self.result, 10, 20, arcade.color.WHITE, 14)

    # def on_mouse_motion(self, x, y, dx, dy):
    #     self.player.center_x = x
    #     self.player.center_y = y

    def on_key_press(self, symbol, modifiers):
        if symbol == 65362:
            self.player.center_y += 20
        elif symbol == 65364:
            self.player.center_y -= 20
        elif symbol == 65361:
            self.player.center_x -= 20
        elif symbol == 65363:
            self.player.center_x += 20

    # def on_key_release(self, symbol, modifiers):
    def move(self, symbol, modifiers):
        while True:
            if symbol == 65362:
                self.player.center_y += 2
            elif symbol == 65364:
                self.player.center_y -= 2
            elif symbol == 65361:
                self.player.center_x -= 2
            elif symbol == 65363:
                self.player.center_x += 2


    def on_update(self, delta_time):
        if arcade.check_for_collision(self.player, self.coin):
            while self.player.data.hp > 0 and self.coin.data.hp > 0:
                self.player.data.hp -= self.coin.data.attack
                self.coin.data.hp -= self.player.data.attack
                print("player", self.player.data.hp)
                print("coin", self.coin.data.hp)
            self.result = "You win!"


window = MyGame()
# t = threading.Thread(target=move(), name='LoopThread')
arcade.run()