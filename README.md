# NanoCards

## Overview

NanoCards is a dungeon RPG card game, where the player selects heroes to take on dungeons and earn loot. Heroes and enemies each have a race, class, and element. Heroes can also be upgraded to increase stats and unlock new abilities. Attaching rings and amulets to heroes may further increase stats or introduce new status effects.

## Details
### Card Types
- Hero
- Enemy

### Token Types 
Tokens can be attached to cards
- Amulet: one amulet can be attached to one hero
- Ring: two rings can be attached to one hero
- Status Effect: any number of status effects can be attached to any hero or enemy
- Stat Modifier: any number of stat modifiers can be attached to any hero or enemy

### Status Effects:
- Burn: this entity takes damage at the end of each turn  and takes 1.25x damage from fire attacks
- Poison: this entity takes damage at the end of each turn
- Frost: this entity moves 50% slower
- Frozen: this entity cannot move
- Stunned: this entity cannot move
- Aggro: this entity must be targeted by enemies, teammates cannot be directly attacked
- Shield: the shield takes damage in place of this entity until it runs out
- Disease: this entity deals .75x damage and takes 1.25x damage
- Marked for Death: all attacks deal double damage to this entity

### Amulet Boosts
- Increase attack: 5-20%
- Increase defense: 5-20%
- Increase health: 5-30%

### Ring Boosts
- Grant status infliction chance:
  - Burn: 5-10%
  - Poison: 5-10% 
  - Frost: 5-10%
  - Disease: 5-10%
- Add dodge chance: 3-7%
- Add lifesteal: 5-20%
- Add crit chance: 5-20%

### Speed
All entities have a base speed that determines turn order. Turn order precedence:
1. base speed
2. attacker (player) or defender (dungeon/npc): attackers move first to break speed ties
3. card order: attackers with the same speed or defenders with the same speed will follow card order 

### Critical Hits
Deal 2x damage, all entities have a base 5% crit chance

### Races
- Human: compatible with all classes and elements
- Dwarf: incompatible with rogue class
- Elf: incompatible with tank class
- Goblin: incompatible with tank class
- Undead: incompatible with light element, disease status effect is flipped (deals 1.25x damage, takes .75x damage), can be a race modifier (e.g. undead goblin, undead monster, etc.)
- Skeleton: incompatible with light element, immune to disease
- Monster: incompatible with healer class
- Giant: incompatible with rogue class, can be a race modifier (e.g. giant elf, giant skeleton), by default acts as a giant human
- Dragon: incompatible with tank class

### Class
- mage: casts spells and deals pure damage (cannot be reduced)
- tank: moves slower, has high health and defense, and takes hits for teammates
- ranger: focuses on ranged damage, moves quickly
- warrior: focuses on melee damage
- rogue: sacrifices bulk for speed and trickery
- healer: heals and supports teammates

### Elements
- fire
- water
- plant
- air
- earth
- electric
- dark
- light

### Elemental Interactions (when attacking):
Strong: deals 1.5x damage
Weak: deals .75x damage
| Element  | Strong Against  | Weak Against           |
|----------|-----------------|------------------------|
| Fire     | Plant, Air      | Fire, Water, Earth     |
| Water    | Fire, Earth     | Water, Plant, Electric |
| Plant    | Water, Electric | Plant, Fire, Air       |
| Air      | Earth, Plant    | Air, Fire, Electric    |
| Earth    | Electric, Fire  | Earth, Water, Air      |
| Electric | Water, Air      | Electric, Plant, Earth |
| Dark     | Light           | Dark                   |
| Light    | Dark            | Light                  |

### Currencies
- coins: used for purchasing consumables
- gems: used for purchasing specialty consumables and unlocking new abilities on heroes
- magic dust: required for leveling up heroes, rings, and amulets
- runes: required for leveling up heroes at later levels

## Heroes
Each hero has a race*, class, and element. Amulets and rings can be attached or unattached to heroes outside of combat at any time. All heroes start at level 1, but can be leveled up using magic dust. In order to level up, the player must have accumulated the proper number of duplicate hero cards for that hero. Each hero begins with one basic attack and an active ability. At level 10 and level 20 (max level**), an additional active ability is unlocked. Heroes may have any number of passive abilities and can unlock further passive abilities at level 10 or 20. A hero's level cannot exceed the player's level.

*some heroes may have up to two races if one is a race modifier
**max level is subject to change as the game develops

### Leveling up
First 14
| Level | Gems | Cards |
|-------|------|-------|
| 1     | 0    | 1     |
| 2     | 2    | 1     |
| 3     | 4    | 2     |
| 4     | 8    | 3     |
| 5     | 16   | 5     |
| 6     | 32   | 8     |
| 7     | 64   | 13    |
| 8     | 128  | 21    |
| 9     | 256  | 34    |
| 10    | 512  | 55    |
| 11    | 1024 | 89    |
| 12    | 2048 | 144   |
| 13    | 4096 | 233   |
| 14    | 8192 | 377   |

15+
| Level | Runes |
|-------|-------|
| 15    | 5     |
| 16    | 10    |
| 17    | 15    |
| 18    | 25    |
| 19    | 40    |
| 20    | 100   |

## Enemies
Like heros, enemies have races, classes, and elements, as well as basic attacks, active abilities, and passive abilities. Although static to the specific dungeon, each enemy also has a level that determines its stats. Although an enemy can exceed the player's level, the dungeon it belongs to cannot.

## Dungeons
Up to 4 heroes can be selected for each dungeon campaign. Dungeons have element themes and generally have a majority of enemies belonging to a certain race. However, elements that differ from the theme can still be present in the dungeon. Each dungeon consists of any number of rooms, where the player earns minor loot after every enemy in that room is defeated. Some rooms may contain shops, chests (better loot), or other surprises in place of enemies, although this is rarer. The last room of the dungeon always contains the boss for that specific dungeon. After the boss is defeated, the player earns a chest. Loot typically follows the elemental theme of the dungeon.
