from entity import Entity

class Hero(Entity):
    file_loc = "entities/heroes"

    def __init__(self, name, race, entity_class, element, health, attack, defense, speed, active_abilities, passive_abilities):
        super().__init__(name, race, entity_class, element, health, attack, defense, speed, active_abilities, passive_abilities)