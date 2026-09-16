import json
from jsonschema import validate

from ability import Ability
from status import Status

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
        self.base_attack = attack
        self.base_defense = defense
        self.base_speed = speed
        self.active_abilities: list[Ability] = []
        for ability in active_abilities:
            self.active_abilities.append(Ability(ability.get("name"), ability.get("type"), ability.get("element"), ability.get("amount"), ability.get("effect"), ability.get("target"), ability.get("energy")))
        self.passive_abilities: list[Ability] = []
        for ability in passive_abilities:
            self.passive_abilities.append(Ability(ability.get("name"), ability.get("type"), ability.get("element"), ability.get("amount")))

        self.health_status_effects: list[Status] = []
        self.attack_status_effects: list[Status] = []
        self.defense_status_effects: list[Status] = []
        self.speed_status_effects: list[Status] = []
        self.movement_status_effects: list[Status] = []
        self.targeting_status_effects: list[Status] = []
        self.EOT_status_effects: list[Status] = []

        self.energy = 0

    @property
    def attack(self):
        mult = 1
        if self.attack_status_effects:
            for status in self.attack_status_effects:
                mult *= status.amount
        return self.base_attack*mult

    @property
    def defense(self):
        mult = 1
        if self.defense_status_effects:
            for status in self.defense_status_effects:
                mult *= status.amount
        return self.base_defense*mult

    @property
    def speed(self):
        mult = 1
        if self.speed_status_effects:
            for status in self.speed_status_effects:
                mult *= status.amount
        return self.base_speed*mult

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

    def get_attacked(self, attacker, ability: Ability) -> bool:
        damage = int(attacker.attack * ability.amount / self.defense)
        damage *= self.get_element_modifier(ability.element, self.element)
        if self.health_status_effects:
            self.health_status_effects[0].duration -= damage
            if self.health_status_effects[0].duration <= 0:
                self.health_status_effects.pop(0)
                return False
        else:
            killed = self.take_damage(damage)
            if not killed:
                for effect in ability.effect:
                    status, duration, amount = effect.split(",")
                    self.set_status(status, duration, amount)
            return killed

    def take_damage(self, damage) -> bool:
        self.health -= damage
        if self.health <= 0:
            return True
        return False

    def get_element_modifier(self, attack_element, defense_element):
        return self._element_interaction[attack_element][defense_element]

    def modify_stats(self, ability: Ability) -> bool:
        for stat in ability.effect:
            if stat == "health":
                self.max_health *= ability.amount
                self.health *= ability.amount
            elif stat == "attack":
                self.base_attack *= ability.amount
            elif stat == "defense":
                self.base_defense *= ability.amount
            elif stat == "speed":
                self.base_speed *= ability.amount

        return False

    def set_status(self, status, duration, amount):
        if status == "Burn":
            self.EOT_status_effects.append(Status("Burn", "EOT", duration, amount))
        elif status == "Poison":
            self.EOT_status_effects.append(Status("Poison", "EOT", duration, amount))
        elif status == "Frost":
            self.speed_status_effects.append(Status("Frost", "Speed", duration, amount))
        elif status == "Frozen":
            self.movement_status_effects.append(Status("Frozen", "Movement", duration, amount))
        elif status == "Stunned":
            self.movement_status_effects.append(Status("Stunned", "Movement", duration, amount))
        elif status == "Aggro":
            self.targeting_status_effects.append(Status("Aggro", "Targeting", duration, amount))
        elif status == "Shield":
            self.health_status_effects.append(Status("Shield", "Health", duration, amount))
        elif status == "DiseasedA":
            self.attack_status_effects.append(Status("Diseased", "Attack", duration, amount))
        elif status == "DiseasedD":
            self.defense_status_effects.append(Status("Diseased", "Defense", duration, amount))
        elif status == "MarkedForDeath":
            self.defense_status_effects.append(Status("Marked for Death", "Defense", duration, amount))

    def apply_status(self, ability: Ability) -> bool:
        for i in ability.effect:
            status,duration = i.split(",")
            self.set_status(status, int(duration), ability.amount)
        return False

    def heal(self, ability: Ability) -> bool:
        self.health = min(self.health + ability.amount, self.max_health)
        return False
        
    def process_ability(self, attacker, ability: Ability) -> bool:
        if ability.type == "attack":
            return self.get_attacked(attacker, ability)
        if ability.type == "modify":
            return self.modify_stats(ability)
        if ability.type == "status":
            return self.apply_status(ability)
        if ability.type == "heal":
            return self.heal(ability)
        return False

    def status_type_tick(self, status_type: list[Status]):
        to_remove = []
        for status in status_type:
            ended = status.tick()
            if ended:
                to_remove.append(status)
        for status in to_remove:
            status_type.remove(status)

    def tick(self):
        self.status_type_tick(self.health_status_effects)
        self.status_type_tick(self.attack_status_effects)
        self.status_type_tick(self.defense_status_effects)
        self.status_type_tick(self.speed_status_effects)
        self.status_type_tick(self.movement_status_effects)
        self.status_type_tick(self.targeting_status_effects)
        self.status_type_tick(self.EOT_status_effects)