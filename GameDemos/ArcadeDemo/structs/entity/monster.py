from structs.entity.base_entity import BaseEntity


class Monster(BaseEntity):

    def __init__(self, attack, hp):
        super().__init__(attack, hp)