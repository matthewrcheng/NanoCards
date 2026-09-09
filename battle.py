import random
from ability import Ability
from hero import Hero


class Battle:

    def __init__(self, heroes: list[Hero], enemies: list[Hero]):
        self.heroes = heroes
        self.enemies = enemies

        self.turn_order = self.__determine_turn_order()

    def __determine_turn_order(self) -> list:
        """
        1. base speed
        2. attacker (player) or defender (dungeon/npc): attackers move first to break speed ties
        3. card order: attackers with the same speed or defenders with the same speed will follow card order
        """ 
        order = []
        for hero in self.heroes:
            order.append((hero, hero.speed, "hero"))

        for enemy in self.enemies:
            order.append((enemy, enemy.speed, "enemy"))

        return sorted(order, key=lambda x: x[1])

    def play(self):
        ended = False
        while not ended:
            ended = self.turn()

    def turn(self):
        # iterate through turn order
        # if hero, get input from user
        # if enemy, determine using algorithm
        killed = []
        for char in self.turn_order:
            if char[2] == "hero":
                target, ability = self.get_user_input(char[0])
                was_killed = target.process_ability(char[0], ability)
                if was_killed:
                    self.enemies.remove(target)
                    killed.append(target)
            else:
                target, ability = self.decide_move(char[0])
                was_killed = target.process_ability(char[0], ability)
                if was_killed:
                    self.heroes.remove(target)
                    killed.append(target)
        to_remove = []
        if len(killed):
            for char in killed:
                for i in range(len(self.turn_order)):
                    if self.turn_order[i][0] == char:
                        to_remove.append(self.turn_order[i])
            for char in to_remove:
                self.turn_order.remove(char)
        if not len(self.heroes):
            print("Enemy wins")
            return True
        if not len(self.enemies):
            print("You win!")
            return True
        return False

    def get_user_input(self, hero: Hero) -> tuple[Hero, Ability]:
        for char in self.heroes:
            print(f"{char.name} {char.element} {char.health}/{char.max_health}")

        for i,enemy in enumerate(self.enemies):
            print(f"{i}: {enemy.name} {enemy.element} {enemy.health}/{enemy.max_health}")
             
        for i,ability in enumerate(hero.active_abilities):
            print(f"{i}: {ability.name} {ability.element}")

        ability_idx = -1
        while ability_idx < 0 or ability_idx >= len(hero.active_abilities):
            ability_idx = int(input("Select ability:"))

        ability = hero.active_abilities[ability_idx]

        target_list = self.enemies
        if ability.type == "attack": # extend possibilities later
            target_list = self.enemies
        else:
            target_list = self.heroes

        target_idx = -1
        while target_idx < 0 or target_idx >= len(target_list):
            target_idx = int(input("Select target:"))

        target = target_list[target_idx]

        print(f"{hero.name} used {ability.name} on {target.name}")

        return target, ability

    def decide_move(self, enemy: Hero) -> tuple[Hero, Ability]:
        ability = random.choice(enemy.active_abilities)

        target_list = self.enemies
        if ability.type == "attack": # extend possibilities later
            target_list = self.heroes
        else:
            target_list = self.enemies

        target = random.choice(target_list)

        print(f"{enemy.name} used {ability.name} on {target.name}")

        return target, ability