class Status:

    def __init__(self, name, type, duration, amount):
        self.name = name
        self.type = type
        self.duration = duration
        self.amount = amount

    def tick(self) -> bool:
        self.duration -= 1
        if self.duration <= 0:
            return True
        return False

burn = Status("Burn", "EOT", 3, 1)
poison = Status("Poison", "EOT", 3, 1)
frost = Status("Frost", "Speed", 3, 0.5)
frozen = Status("Frozen", "Movement", 2, 1)
stunned = Status("Stunned", "Movement", 2, 1)
aggro = Status("Aggro", "Targeting", 2, 1)
shield = Status("Shield", "Health", 5, 1)
disease = Status("Diseased", "Attack", 3, 0.75)
disease2 = Status("Diseased", "Defense", 3, 0.8)
marked_for_death = Status("Marked for Death", "Defense", 3, 0.5)