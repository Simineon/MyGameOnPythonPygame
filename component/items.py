from globals import *
from sprite import *
from player import *

class Item:
    def __init__(self, name: str = 'default', quantity: int = 0) -> None:
        self.name = name
        self.quantity = quantity
    def use(self, *arg, **kwargs):
        pass
    def attack(self, *args, **kwargs):
        pass
    def __str__(self):
        return f'Name: {self.name}, Quatity: {self.quantity}'

class BlockItem(Item):
    def __init__(self, name: str,quantity: int = 0) -> None:
        super().__init__(name, quantity)
    def use(self, player, position: tuple):
        if self.quantity > 0:
            items[self.name].use_type([player.group_list[group] for group in items[self.name].groups], player.textures[self.name], position, self.name)
            self.quantity -= 1
            if self.quantity <= 0:
                self.name = 'default'
        else:
            self.name = "default"

class ShortSwordCItem(Item):
    def __init__(self, name: str = "default", quantity: int = 0) -> None:
        super().__init__(name, quantity)
    def use(self, player, position: tuple):
        print('useing sword')
    def attack(self, player, target):
        target.kill()

class ItemDate:
    def __init__(self, name: str, quantity: int = 1, groups: list[str] = ['sprites', 'block_group'], use_type: Entity = Entity, item_type: Item = Item) -> None:
        self.name = name
        self.quantity = quantity
        self.groups = groups
        self.use_type = use_type
        self.item_type = item_type
class ItemAirDate:
    def __init__(self, name: str, quantity: int = 1, groups: list[str] = ['sprites', 'air_group'], use_type: Entity = Entity, item_type: Item = Item) -> None:
        self.name = name
        self.quantity = quantity
        self.groups = groups
        self.use_type = use_type
        self.item_type = item_type


items:dict[str,ItemDate] = {
    'grass':ItemDate('grass', item_type=BlockItem),
    'dirt':ItemDate('dirt', item_type=BlockItem),
    'stone':ItemDate('stone', item_type=BlockItem),
    'deamond':ItemDate('deamond', item_type=BlockItem),
    'short_sword':ItemDate('short_sword', item_type=ShortSwordCItem),
    'tree':ItemAirDate('short_sword', item_type=BlockItem),
    'wood':ItemDate('wood', item_type=BlockItem),
}