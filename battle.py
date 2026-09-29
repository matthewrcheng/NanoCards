import random
import socket
from ability import Ability
from entity import Hero


class Battle:

    def __init__(self, heroes: list[Hero], enemies: list[Hero], local: bool = False):
        self.heroes = heroes
        self.enemies = enemies

        self.local = local
        if not self.local:
            self.conn = None
            self.address = None
            self.host = '127.0.0.1'  # loopback address for local testing
            self.port = 5000  # initiate port no above 1024

            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP socket
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow port reuse immediately after server shutdown
            self.server_socket.bind((self.host, self.port))  # bind host address and port together


        self.turn_order = self.__determine_turn_order()

    def __determine_turn_order(self) -> list[tuple[Hero, int, str]]:
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

        sorted_order = sorted(order, key=lambda x: x[1], reverse=True)

        print(sorted_order)

        return sorted_order

    def play(self):
        # accept connections for play
        self.server_socket.listen(5)  # queue up to 5 connection requests
        self.conn, self.address = self.server_socket.accept()  # wait for client and get connection
        print("Connection from: " + str(self.address))

        ended = False
        while not ended:
            ended = self.turn()

        self.conn.close()  # close the connection
        self.conn = None
        self.address = None
        self.server_socket.close()  # close the listening socket

    def check_end(self):
        if not len(self.heroes):
            data = "Enemy wins"
            if self.local:
                print(data)
            else:
                self.conn.sendall(f"4{data}".encode())  # send data to the client
            return True
        if not len(self.enemies):
            data = "You win!"
            if self.local:
                print(data)
            else:
                self.conn.sendall(f"4{data}".encode())  # send data to the client
            return True
        return False

    def turn(self):
        # iterate through turn order
        # if hero, get input from user
        # if enemy, determine using algorithm
        killed = []
        for char in self.turn_order:
            if char[0] in killed or char[0].movement_status_effects:
                continue
            if char[2] == "hero":
                targets, ability = self.get_user_input(char[0])
            else:
                targets, ability = self.decide_move(char[0])
            for target in targets:
                was_killed = target.process_ability(char[0], ability)
                if was_killed:
                    if char[2] == "hero":
                        self.enemies.remove(target)
                    else:
                        self.heroes.remove(target)
                    killed.append(target)
            if self.check_end():
                return True
        for char in self.turn_order:
            if char[0].EOT_status_effects:
                for status in char[0].EOT_status_effects:
                    was_killed = char[0].take_damage(status.amount)
                    if was_killed:
                        if char[2] == "hero":
                            self.heroes.remove(target)
                        else:
                            self.enemies.remove(target)
                        killed.append(target)
            if self.check_end():
                return True
            char[0].tick()
        to_remove = []
        if len(killed):
            for char in killed:
                for i in range(len(self.turn_order)):
                    if self.turn_order[i][0] == char:
                        to_remove.append(self.turn_order[i])
            for char in to_remove:
                self.turn_order.remove(char)
        return self.check_end()

    def get_user_input(self, hero: Hero) -> tuple[Hero, Ability]:
        if self.local:
            return self.get_user_input_cli(hero)
        else:
            return self.get_user_input_client(hero)

        
    def get_user_input_client(self, hero: Hero) -> tuple[Hero, Ability]:
        # send the client information related to making their selection

        data = "1"
        for char in self.heroes:
            data += f"{char.name} {char.element} {char.health}/{char.max_health}\n"

        data += ","

        for i,enemy in enumerate(self.enemies):
            data += f"{i}: {enemy.name} {enemy.element} {enemy.health}/{enemy.max_health}\n"

        data += ","
                
        for i,ability in enumerate(hero.active_abilities):
            data += f"{i}: {ability.name} {ability.element}\n"

        data += f",{len(hero.active_abilities)}"

        self.conn.sendall(data.encode())  # send data to the client

        ability_idx = -1
        while ability_idx < 0 or ability_idx >= len(hero.active_abilities):
            raw = self.conn.recv(1024)  # read the client's selection
            try:
                ability_idx = int(raw.decode('utf-8'))
            except UnicodeDecodeError:
                print(f"Received non-UTF-8 data from {self.address}, skipping")
            except Exception as e:
                print(f"Bad response from {self.address}: {e}")
            print("user selected: " + str(ability_idx))

        ability = hero.active_abilities[ability_idx]

        if ability.target == "Opponent":

            for enemy in self.enemies:
                if enemy.targeting_status_effects:
                    return [enemy], ability

            data = "2"
            for i,char in enumerate(self.enemies):
                data += f"{i}: {char.name} {char.element} {char.health}/{char.max_health}\n"

            data += f",{len(self.enemies)}"

            self.conn.sendall(data.encode())

            target_idx = -1
            while target_idx < 0 or target_idx >= len(self.enemies):
                raw = self.conn.recv(1024)  # read the client's selection
                try:
                    target_idx = int(raw.decode('utf-8'))
                except UnicodeDecodeError:
                    print(f"Received non-UTF-8 data from {self.address}, skipping")
                except Exception as e:
                    print(f"Bad response from {self.address}: {e}")
                print("user selected: " + str(target_idx))

            target = self.enemies[target_idx]

            data = f"3{hero.name} used {ability.name} on {target.name}"
            self.conn.sendall(data.encode())  # send data to the client

            return [target], ability

        if ability.target == "Opponents":
            data = f"3{hero.name} used {ability.name}"
            self.conn.sendall(data.encode())
            return self.enemies, ability

        if ability.target == "Self":
            data = f"3{hero.name} used {ability.name}"
            self.conn.sendall(data.encode())
            return [hero], ability

        if ability.target == "Teammate":

            data = "2"
            for i,char in enumerate(self.heroes):
                data += f"{i}: {char.name} {char.element} {char.health}/{char.max_health}\n"

            data += f",{len(self.heroes)}"
            
            self.conn.sendall(data.encode())

            target_idx = -1
            while target_idx < 0 or target_idx >= len(self.heroes):
                raw = self.conn.recv(1024)
                try:
                    target_idx = int(raw.decode('utf-8'))
                except UnicodeDecodeError:
                    print(f"Received non-UTF-8 data from {self.address}, skipping")
                except Exception as e:
                    print(f"Bad response from {self.address}: {e}")
                print("user selected: " + str(target_idx))

            target = self.heroes[target_idx]

            data = f"3{hero.name} used {ability.name} on {target.name}"
            self.conn.sendall(data.encode())

            return [target], ability

        if ability.target == "Team":
            data = f"3{hero.name} used {ability.name}"
            self.conn.sendall(data.encode())
            return self.heroes, ability

        return random.choice(self.enemies), ability


    def get_user_input_cli(self, hero: Hero) -> tuple[Hero, Ability]:
        for char in self.heroes:
            print(f"{char.name} {char.element} {char.health}/{char.max_health}")

        for i,enemy in enumerate(self.enemies):
            print(f"{i}: {enemy.name} {enemy.element} {enemy.health}/{enemy.max_health}")
             
        for i,ability in enumerate(hero.active_abilities):
            print(f"{i}: {ability.name} {ability.element}")

        ability_idx = -1
        while ability_idx < 0 or ability_idx >= len(hero.active_abilities):
            try:
                ability_idx = int(input("Select ability:"))
            except ValueError:
                print(f"Please input only a number 0-{len(hero.active_abilities)-1}")
                ability_idx = -1
            except Exception:
                print(f"Unexptected Error: Please try again")
                ability_idx = -1

        ability = hero.active_abilities[ability_idx]

        if ability.target == "Opponent":

            target_idx = -1
            while target_idx < 0 or target_idx >= len(self.enemies):
                try:
                    target_idx = int(input("Select target:"))
                except ValueError:
                    print(f"Please input only a number 0-{len(self.enemies)-1}")
                    target_idx = -1
                except Exception:
                    print(f"Unexptected Error: Please try again")
                    target_idx = -1

            target = self.enemies[target_idx]

            print(f"{hero.name} used {ability.name} on {target.name}")

            return [target], ability
        
        if ability.target == "Opponents":
            print(f"{hero.name} used {ability.name}")
            return self.enemies, ability

        if ability.target == "Self":
            print(f"{hero.name} used {ability.name}")
            return [hero], ability

        if ability.target == "Teammate":
            target_idx = -1
            while target_idx < 0 or target_idx >= len(self.heroes):
                try:
                    target_idx = int(input("Select target:"))
                except ValueError:
                    print(f"Please input only a number 0-{len(self.heroes)-1}")
                    target_idx = -1
                except Exception:
                    print(f"Unexptected Error: Please try again")
                    target_idx = -1

            target = self.heroes[target_idx]

            print(f"{hero.name} used {ability.name} on {target.name}")

            return [target], ability

        if ability.target == "Team":
            print(f"{hero.name} used {ability.name}")
            return self.heroes, ability

        return random.choice(self.enemies), ability


    def decide_move(self, enemy: Hero) -> tuple[Hero, Ability]:
        ability = random.choice(enemy.active_abilities)

        target_list = self.enemies
        if ability.type == "attack": # extend possibilities later
            target_list = self.heroes
        else:
            target_list = self.enemies

        target = random.choice(target_list)

        message = f"{enemy.name} used {ability.name} on {target.name}"
        if self.local:
            print(message)
        else:
            self.conn.sendall(message.encode())

        return [target], ability