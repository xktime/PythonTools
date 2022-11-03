from structs.entity.base_entity import BaseEntity


class Player(BaseEntity):

    def __init__(self, attack, hp):
        super().__init__(attack, hp)
