from battle import Battle
from hero import Hero
from enemy import Enemy

def main():
    ds = Hero.from_json("drowned_sailor")
    elfina = Hero.from_json("elfina")
    goblino = Hero.from_json("goblino")
    skulitan = Hero.from_json("skulitan")

    heroes = [ds, elfina, goblino, skulitan]

    msw1 = Enemy.from_json("magma_skeletal_warrior")
    msw2 = Enemy.from_json("magma_skeletal_warrior")
    msw3 = Enemy.from_json("magma_skeletal_warrior")
    msw4 = Enemy.from_json("magma_skeletal_warrior")

    enemies = [msw1, msw2, msw3, msw4]

    battle = Battle(heroes, enemies)

    battle.play()



if __name__ == "__main__":
    main()
