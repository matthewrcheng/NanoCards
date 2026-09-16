class Ability:

    def __init__(self, name: str, ability_type: str, element: str, amount: float, effect: list, target: str, energy: float):
        self.name = name
        self.type = ability_type
        self.element = element
        self.amount = amount
        self.effect = effect
        self.target = target
        self.energy = energy