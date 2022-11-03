class BaseEntity(object):

    def __init__(self, attack, hp):
        self.attack = attack
        self.hp = hp

    def print_hp(self):
        print(self.hp)