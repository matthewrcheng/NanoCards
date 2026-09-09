import json
from jsonschema import validate

from ability import Ability

class Hero:
    _element_interaction = {
        'Fire': {
            'Fire': 0.75,
            'Water': 0.75, 
            'Plant': 1.5,
            'Air': 1.5,
            'Earth': 0.75,
            'Electric': 1,
            'Light': 1,
            'Dark': 1
        },
        'Water': {
            'Fire': 1.5,
            'Water': 0.75, 
            'Plant': 0.75,
            'Air': 1,
            'Earth': 1.5,
            'Electric': 0.75,
            'Light': 1,
            'Dark': 1
        }, 
        'Plant': {
            'Fire': 0.75,
            'Water': 1.5, 
            'Plant': 0.75,
            'Air': 0.75,
            'Earth': 1,
            'Electric': 1.5,
            'Light': 1,
            'Dark': 1
        },
        'Air': {
            'Fire': 0.75,
            'Water': 1, 
            'Plant': 1.5,
            'Air': 0.75,
            'Earth': 1.5,
            'Electric': 0.75,
            'Light': 1,
            'Dark': 1
        },
        'Earth': {
            'Fire': 1.5,
            'Water': 0.75, 
            'Plant': 1,
            'Air': 0.75,
            'Earth': 0.75,
            'Electric': 1.5,
            'Light': 1,
            'Dark': 1
        },
        'Electric': {
            'Fire': 1,
            'Water': 1.5, 
            'Plant': 0.75,
            'Air': 1.5,
            'Earth': 0.75,
            'Electric': 0.75,
            'Light': 1,
            'Dark': 1
        },
        'Light': {
            'Fire': 1,
            'Water': 1, 
            'Plant': 1,
            'Air': 1,
            'Earth': 1,
            'Electric': 1,
            'Light': 0.63,
            'Dark': 1.25
        },
        'Dark': {
            'Fire': 1,
            'Water': 1, 
            'Plant': 1,
            'Air': 1,
            'Earth': 1,
            'Electric': 1,
            'Light': 1.25,
            'Dark': 0.63
        }
    }

    def __init__(self, name: str, race: str, entity_class: str, element: str, health: int, attack: int, defense: int, speed: int, active_abilities: list[dict], passive_abilities: list[dict]):
        self.name = name
        self.race = race
        self.entity_class = entity_class
        self.element = element
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.active_abilities: list[Ability] = []
        for ability in active_abilities:
            self.active_abilities.append(Ability(ability.get("name"), ability.get("type"), ability.get("element"), ability.get("amount")))
        self.passive_abilities: list[Ability] = []
        for ability in passive_abilities:
            self.passive_abilities.append(Ability(ability.get("name"), ability.get("type"), ability.get("element"), ability.get("amount")))

        self.status_effects = []

    @classmethod
    def from_json(cls, name):
        schema = {}
        with open("entity_schema.json", "r") as f:
            schema = json.load(f)

        data = {}
        with open(f"heroes/{name}.entity.json", "r") as f:
            data = json.load(f)

        try:
            validate(instance=data, schema=schema)
            print(f"Loaded {name}")
            return cls(
                name = data.get("name"),
                race = data.get("race"),
                entity_class = data.get("class"),
                element = data.get("element"),
                health = data.get("health"),
                attack = data.get("attack"),
                defense = data.get("defense"),
                speed = data.get("speed"),
                active_abilities = data.get("active_abilities"),
                passive_abilities = data.get("passive_abilities")
            )
        except Exception as e:
            print(f"Error loading {name}: {e}")
        return None

    def take_damage(self, attacker, ability: Ability):
        damage = int(attacker.attack * ability.amount / self.defense)
        damage *= self.get_element_modifier(ability.element, self.element)
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def get_element_modifier(self, attack_element, defense_element):
        return self._element_interaction[attack_element][defense_element]
        
    def process_ability(self, attacker, ability: Ability):
        if ability.type == "attack":
            return self.take_damage(attacker, ability)
        else:
            return False
