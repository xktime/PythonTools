import random

import arcade
from arcade import key, Sprite

from structs.entity.monster import Monster
from structs.entity.player import Player


class GameWindow(arcade.Window):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__(self.WIDTH, self.HEIGHT, "SuperKiller")
        arcade.set_background_color(arcade.color.WHITE)
        self.player = arcade.Sprite("resources/player.png", 0.5)
        self.player.center_x = 400
        self.player.center_y = 300
        self.player.entity = Player(1, 500)
        self.monster = arcade.Sprite("resources/monster.png", 0.25)
        self.monster.center_x = 100
        self.monster.center_y = 100
        self.monster.entity = Monster(1, 50)

    def on_draw(self):
        arcade.start_render()
        self.monster.draw()
        self.player.draw()
        arcade.draw_text(self.player.entity.hp, 100, 20, arcade.color.WINE, 14)
        arcade.draw_text(self.monster.entity.hp, 20, 20, arcade.color.WINE, 14)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.player.center_y += 20
        elif symbol == key.DOWN:
            self.player.center_y -= 20
        elif symbol == key.LEFT:
            self.player.center_x -= 20
        elif symbol == key.RIGHT:
            self.player.center_x += 20

    def on_update(self, delta_time):
        if arcade.check_for_collision(self.player, self.monster):
            self.fight(self.monster)

    def fight(self, monster: Sprite):
        self.player.entity.hp -= monster.entity.attack
        monster.entity.hp -= self.player.entity.attack
        die = self.player.entity.hp <= 0 or monster.entity.hp <= 0
        if die:
            win = self.player.entity.hp > 0
            if win:
                monster.remove_from_sprite_lists()
            else:
                self.player.remove_from_sprite_lists()
            self.fresh_monster()

    def fresh_monster(self):
        self.monster = arcade.Sprite("resources/monster.png", 0.25)
        self.monster.center_x = random.randint(1, self.WIDTH)
        self.monster.center_y = random.randint(1, self.HEIGHT)
        self.monster.entity = Player(1, 50)
        self.monster.draw()
