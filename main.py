from dataclasses import dataclass
from random import choice
import random
import pickle
import os
from typing import List, Tuple

@dataclass
class Player:
    name: str
    max_health: int
    health: int
    max_mana: int
    mana: int
    p_class: str
    advanced_class: str
    level: int
    xp: int
    gold: int
    orb: int
    curr_weapon: str
    health_potion: int
    mana_potion: int
    skills: list
    inventory: list
    sideloc: str
    end: str

skill_damage = {
    "Vertical Arc": 8,
    "Fireball": 8,
    "Long Shot": 8,
    "Howling Octave": 15,
    "Lunar Tempest": 15,
    "Sneak Attack": 15,
    "Deadly Sins": 22,
    "Soul Rain": 22,
    "Sinister Strike": 22,
}
skill_cost = {
    "Vertical Arc": 5,
    "Fireball": 5,
    "Long Shot": 5,
    "Howling Octave": 10,
    "Lunar Tempest": 10,
    "Sneak Attack": 10,
    "Deadly Sins": 15,
    "Soul Rain": 15,
    "Sinister Strike": 15,
}
weapons = {"Rusted Sword": 5, "Short Sword": 14, "Claymore": 20, "God Sword": 60}

inventory = ["Rusted Sword", "God Sword"]

towns = {
    "Waverly": "Situated on the base of a geyser field, the hamlet of Waverly is home to vikings lead by Lord Lockridge. \nThis hamlet wasn't built by a geyser field by accident, as it has an abundance of minerals, which is of great importance to the people of Waverly and its success. \nThe hamlet itself looks unattractive. With its rusted rooftops, rusted walls and whistling wind, Waverly has a gloomy atmosphere. \nWaverly has a mending economy, which is mainly supported by woodcrafting, jewelcrafting and baking. But their biggest strengths are alchemy and advanced medicine. \nHowever, Waverly lacks people skilled in animal breeding.\n[Road1(to Kingston or Oakland), Forrest1, Jagged Tombs]",
    "Oakland": "Forged next to a cave, the village of Oakland is home to elves lead by Supervisor Ninleyn. \nThis village wasn't built by a cave by accident, as it has fertile soils, which is of great importance to the people of Oakland and its success. \nThe village itself looks sublime. With its elm wood rooftops, ironwood walls and lucious gardens, Oakland has a charming atmosphere. \nOakland has a wounded economy, which is mainly supported by fletching, trade and baking. But their biggest strengths are deadly archers and delicate woodcrafting. \nHowever, Oakland lacks people skilled in alchemy.\n[Road1(to Riverside or Waverly), Forrest1, Lifeless Labyrinth]",
    "Kingston": "Formed inside a field, the burg of Kingston is home to orcs lead by Marshal Grikug. \nThis burg wasn't built by a field by accident, as it has rare plants, which is of great importance to the people of Kingston and its success. \nThe burg itself looks delightful. With its silky oak wood rooftops, lavastone walls and frozen lakes, Kingston has a pleasing atmosphere. \nKingston has a declining economy, which is mainly supported by baking, alchemy and thieving. But their biggest strengths are sophisticated cooking and skilled fighters. \nHowever, Kingston lacks people skilled in animal training.\n[Road1(to Waverly or Riverside), Forrest1, Shadowed Dungeon]",
    "Riverside": "Based on the Northern side of a waterfall, the port of Riverside is home to high elves lead by Director Alwin. \nThis port wasn't built by a waterfall by accident, as it has unique wildlife, which is of great importance to the people of Riverside and its success. \nThe port itself looks impressive. With its cypress wood rooftops, mahogany wood walls and silent mountain range, Riverside has a intriguing atmosphere. \nRiverside has a hurting economy, which is mainly supported by hunting, thieving and beer brewing. But their biggest strengths are skilled fighters and intricate fletching techniques. \nHowever, Riverside lacks people skilled in tailoring.\n[Road1(to Oakland or Kingston), Forrest1, Dreadful Tunnels]",
    "Jagged Tombs": "A short worn statue in a murky woodlands marks the entrance to this dungeon.\n[Waverly]",
    "Dreadful Tunnels": "A grand fallen temple in a gloomy grove marks the entrance to this dungeon.\n[Riverside, Entrance]",
    "Shadowed Dungeon": "A wide worn statue in a somber boulder field marks the entrance to this dungeon.\n[Kingston]",
    "Lifeless Labyrinth": "A tall broken statue in a misty woodlands marks the entrance to this dungeon.\n[Oakland]",
    "Crypt of the Conquered King": "A Magic Veil was lifted, so now the entrance is revealed. \nA huge ancient monument of a dragon is the entrance to this dungeon.\n[Forrest1, Forrest3, Enterance]",
    "Forrest2": "There is a weird magical veil here. You can tell that it is close to being shattered. You can't tell exactly where the magic is at, or where it's coming from.",
    "Road1": "It is sort of peaceful, nothing really happens close to towns.\n[Road2, name of last town]",
    "Road2": "You hear birds, squirrels, and other wildlife. Nothing should happen on a road anyway. You come to a place where a small fire is on the side of the road with a man, and woman. They wave at you and say to be careful. You never know what could happen.\n[Road1, Road3]",
    "Road3": "It is sort of peaceful, nothing really happens close to towns.[Road2, name of next town]",
}

forrest = {
    1: "As you walk through the path, you have a feeling of being watched. You start to hear the leaves near you crackle. As you hear this, a squirrel pops out and scurries across the path.",
    2: "As you are walking, you hear leaves in the trees to your right. The birds are singing, and flowers are blooming. On days like this. People like you. Shouldn't be adventuring, it is so nice outside.",
    3: "You notice to your right a small clearing for a camp. There is a small tent there. As you pass by, a goblin comes out and attacks.",
    4: "On your way, you notice a patch of grass in your way, and hear a small cry coming from it. As you travel through it, you are attacked by a few slimes.",
}


mvmt = [
    ("Waverly", "Road1"),
    ("Waverly", "Forrest1"),
    ("Waverly", "Jagged Tombs"),
    ("Riverside", "Dreadful Tunnels"),
    ("Riverside", "Road1"),
    ("Riverside", "Forrest1"),
    ("Oakland", "Road1"),
    ("Oakland", "Forrest1"),
    ("Oakland", "Lifeless Labyrinth"),
    ("Kingston", "Road1"),
    ("Kingston", "Forrest1"),
    ("Kingston", "Shadowed Dungeon"),
    ("Road1", "Road2"),
    ("Road1", "Waverly"),
    ("Road1", "Riverside"),
    ("Road1", "Oakland"),
    ("Road1", "Kingston"),
    ("Forrest1", "Forrest2"),
    ("Forrest1", "Waverly"),
    ("Forrest1", "Riverside"),
    ("Forrest1", "Oakland"),
    ("Forrest1", "Kingston"),
    ('Forrest2', 'Forrest1'),
    ('Forrest2', 'Forrest3'),
    ("Road3", "Road2"),
    ("Road3", "Waverly"),
    ("Road3", "Riverside"),
    ("Road3", "Oakland"),
    ("Road3", "Kingston"),
    ("Forrest3", "Forrest2"),
    ("Forrest3", "Waverly"),
    ("Forrest3", "Riverside"),
    ("Forrest3", "Oakland"),
    ("Forrest3", "Kingston"),
    ("Road2", "Road3"),
    ("Road2", "Road1"),
    ('Crypt of the Conquered King', 'Forrest1'),
    ('Crypt of the Conquered King', 'Forrest3'),
    ("Jagged Tombs", "Waverly"),
    ("Dreadful Tunnels", "Riverside"),
    ("Lifeless Labyrinth", "Oakland"),
    ("Shadowed Dungeon", "Kingston"),
]

dreadfull_tunn_des = {
    "Entrance": "Beyond the fallen temple lies a small, dank room. It's covered in broken pottery, dirt and broken stone. Your torch allows you to see broken mining equipment, tattered and spoiled by time itself. Further ahead are three paths, and the left is a dead end. \n[Hall1, Hall2, Exit]",
    "Hall1": 'It is a small hallway with one room at the end of it. The door says "tokeq" \n[Entrance, Room1]',
    "Hall2": 'It is a small hallway with one room at the end of it. The door says "tokeq" \n[Entrance, Room2, Room3]',
    "Hall3": 'It is a small hallway with one room at the end of it. The door says "tokeq" \n[Room2, Room1]',
    "Room1": "You enter a semi dark area. The floor is cracked and broken in spots. \n[Hall3, Hall2]",
    "Room2": "This room is a small room with barren walls. The walls look like they have had oil on them for a while. There is one table in the room with an old paper dating 987 on it. There is nothing else in the room.\n[Hall2, Hall3]",
    "Room3": "It is a small humid room. You notice there is water running up the wall, Not down like you would expect. \n[Hall2]",
    "Room4": "You enter a humid area. Piles and piles of gold lie in the center, several skeletons lie next to it. \n[Hall5, Hall2]",
    "Hall5": "This hallway is decorated in small nests, large nests, and one huge nest. At a few points in the hall, you can tell where some rooms or hallways were, but the roof is caved in at those places. There are a few rooms and a hallway. \n[Room4, Hall4, Room5, Hall6, Room9]",
    "Hall4": "This is a small hallway leading to a small room.[Hall5, Room7]",
    "Room 7": "The room is small, as it looks like an abandoned labratory.[Hall4]",
    "Room5": "This is a small room, you can see that the papers and books are all from a previous era.\n[Hall5]",
    "Hall6": "It is a small hallway with torches on the sides.\n[Hall5, Room6]",
    "Room6": "A small room with standing water. As you enter, small mice scurry around.\n[Hall6, Hall7]",
    "Hall7": "The small hallway splits off into two paths. One however, is blocked off by debris.\n[Room6, Hall8]",
    "Hall8": "The small hallway is leading into a small room\n[Room9, Hall7]",
    "Room9": "You eventually make it to what is likely the final room. A huge wooden door blocks your path. Various odd symbols are all over it, somehow untouched by time and the elements. You step closer to inspect it and.. wait.. you hear a loud bang in the distance from which you came. Out of panic, you turn around to claw at the doors to find that they are now wide open. You enter.",
    "BossRoom": "The doors slam shut behind you. \nThe room is huge and lined with nests small, large, huge, and one big enough to fit an elephant. You hear a loud sound, resembling a rat, from above. As you hear this, a rat the size of a car falls from the ceiling.",
}

dreadfull_tunnels:List[Tuple] = [
    ("Entrance", "Exit"),
    ("Entrance", "Hall1"),
    ("Entrance", "Hall2"),
    ("Hall1", "Entrance"),
    ("Hall1", "Room1"),
    ("Hall2", "Entrance"),
    ("Hall2", "Room2"),
    ("Hall2", "Room3"),
    ("Hall3", "Room1"),
    ("Hall3", "Room2"),
    ("Hall4", "Hall5"),
    ("Hall4", "Room7"),
    ("Hall5", "Room4"),
    ("Hall5", "Hall4"),
    ("Hall5", "Room5"),
    ("Hall5", "Hall6"),
    ("Hall5", "Room9"),
    ("Hall6", "Hall5"),
    ("Hall6", "Room6"),
    ("Hall7", "Room6"),
    ("Hall7", "Hall8"),
    ("Hall8", "Room9"),
    ("Hall8", "Hall7"),
    ("Room1", "Hall3"),
    ("Room1", "Hall2"),
    ("Room2", "Hall2"),
    ("Room2", "Hall3"),
    ("Room3", "Hall2"),
    ("Room4", "Hall5"),
    ("Room4", "Hall6"),
    ("Room5", "Hall5"),
    ("Room6", "Hall6"),
    ("Room7", "Hall7"),
    ("Room9", "BossRoom"),
    ("BossRoom", "Exit"),
]


BossDungeonMvmt = {
    'Entrance': "A Magic Veil was lifted, so now the entrance is revealed. \nA huge ancient monument of a dragon is the entrance to this dungeon. \nAs you pass the monument, it looks at you and roars. It then goes back to being a monument.\n[Room1, Exit]",
    'Room1': 'The room is a small entrance room. The small doors look to be that of dwarven status. The floor and walls seem to be stone that has been there since the time of the Gods. You see farther in that there are two paths with rooms on the end of them. One path is blocked by iron bars. In the center, you see a slot for mail, a place to open and shoot arrows from, and a place at the bottom for sliding small sacks of food through.\n[Entrance, Room2]',
    'Room2': 'In the center of the room, there is a table with small health and mana potions. You think to yourself that it would be a waste to leave them, so you take them.\n[Room1, Room3]',
    'Room3': 'This room is a large, rounded, hallway room. If you do not know what a rounded hallway room is, it is a circular hallway that has a room in the very center. There are two chests in this room with a key two large health potions, a mana potion, and a few pieces of gold.\n\nYou take the gold, key, and potions.[Room5, Room4, Room8, Hall1, Room2]',
    'Hall1': 'This hallway is small and round. It leads to a small room that is empty with a large chasm opened up at the end below a crack. Past the crack, is a room with a chest that looks like it has not been touched in years.\n[Room7, Room3]',
    'Room7': 'As you jump across the chasm, you hear a loud roar below as fire and smoke come up from the chasm. After a few seconds, the smoke disapates. The chest contains a pile of gold and a weird looking key.\n[Hall1]',
    'Room4': 'In this room, there are just empty boxes and crates. There are also tables and chairs.\n[Room3]',
    'Room5': 'The room has a square hole in the center. It leads down to the chasm below. Around it and on the ceiling, you can see burn marks and soot.\n[Room3]',
    'Room8': 'In this room, you see stairs leading to the chasm below.\n[Chasm, Room3]',
    'Chasm': "As you decend the stairs, you see a huge dragon skeleton. The skeleton looks like it hasn't been touched in hundreds of years. You do notice a small mark on the skull. You go closer to look at it, and as you do, the dragon skeleton risies and roars."
}

shop_inv = [
    "1 Health Potion",
    "3 Health Potions",
    "5 Health Potions",
    "7 Health Potions",
    "1 Mana Potion",
    "3 Mana Potions",
    "5 Mana Potions",
    "7 Mana Potions",
    "Short Sword",
    "Claymore"
]
shop_price = [20,35,75,100,20,35,75,100,20,30]


def shop(player:Player) -> None:
    i=0
    print("Welcome to the shop.\n\n")
    for l,r in zip(shop_inv, shop_price):
        print(l,r)
    buy=input("> ").title()
    for item in shop_inv:
        if item == buy:
            if player.gold>=shop_price[i]:
                if buy == "1 Health Potion":
                    player.health_potion += 1
                elif buy == "3 Health Potions":
                    player.health_potion += 3
                elif buy == "5 Health Potions":
                    player.health_potion += 5
                elif buy == "7 Health Potions":
                    player.health_potion += 7
                elif buy == "1 Mana Potion":
                    player.mana_potion += 1
                elif buy == "3 Mana Potions":
                    player.mana_potion += 3
                elif buy == "5 Mana Potions":
                    player.mana_potion += 5
                elif buy == "7 Mana Potions":
                    player.mana_potion += 7
                elif buy == "Short Sword":
                    player.inventory.append("Short Sword")
                elif buy == "Claymore":
                    player.inventory.append("Claymore")
                else:
                    print('popsicle')
            else:
                print("You don't have enough gold.")
        print("We don't have that here.")

Boss_val:List[Tuple] = [
    ('Entrance', 'Room1'),
    ('Room1', 'Entrance'),
    ('Room1', 'Room2'),
    ('Room2', 'Room3'),
    ('Room2', 'Room1'),
    ('Room3', 'Room2'),
    ('Room3', 'Room4'),
    ('Room3', 'Room5'),
    ('Room3', 'Hall1'),
    ('Room3', 'Room8'),
    ('Hall1', 'Room7'),
    ('Hall1', 'Room3'),
    ('Room8', 'Chasm'),
    ('Room2', 'Room3'),
    ('Room4', 'Room3'),
    ('Room5', 'Room3'),
    ('Room8', 'Room3'),
    ('Entrance', 'Exit'),
    ('Room7', 'Hall1')

]

def use_potion(player: Player) -> None:
    print("\nDo you want to use a [Health Potion] or [Mana Potion]?")
    action = input("> ").title()
    if player.health_potion == 0 and player.mana_potion == 0:
        print("You have no potions.")
    elif action == "Health Potion":
        print("You drink a health potion, and recovered 30 health!")
        player.health += 30
        player.health_potion -= 1
    elif action == "Mana Potion":
        print("You drink a mana potion, and recovered 30 mana!")
        player.mana += 30
        player.mana_potion -= 1

def DragonFight(player: Player) -> None:
    print(
        "As you walk into the room, you see something move. You prepare your weapon just in case but are forced to dodge as a fireball lands right where you were. Standing back up, you see what the monster is. A skeletal dragon that is ready to attack!"
    )
    monsterhp = 300
    monster = "Skeletal Dragon"
    while monsterhp > 0 and player.health > 0:
        print(f"Player Health: {player.health}")
        print(f"Player Mana: {player.mana}")
        print(f"Monster Health: {monsterhp}")
        if player.p_class == "Knight":
            move = input(
                "\nDo you want to [Attack], use a [Sword Skill], or use a [Potion]? "
            ).title()
            if move == "Sword Skill" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Sword Skill":
                print(player.skills)
                skill = sword_skill_input()
                if skill in player.skills:
                    player_damage = skill_damage[skill]
                    monsterhp -= player_damage
                    print(f"You used {skill}, it does {player_damage} damage.")
                    player.mana -= skill_cost[skill]
            elif move == "Attack":
                player_damage = weapons[player.curr_weapon]
                print(f"You used {move}, it does {player_damage} damage.")
                monsterhp -= player_damage
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(20,40)
            print(
                f"\nIt is now the {monster}'s turn.\nThe {monster} attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
        elif player.p_class == "Mage":
            print("Do you want to [Attack], use a [Spell], or use a [Potion]")
            move = input("> ").title()
            if move == "Spell" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Spell":
                print(player.skills)
                spell = spell_input()
                if spell in player.skills:
                    player_damage = skill_damage[spell]
                    monsterhp -= player_damage
                    print(f"You used {spell}, it does {player_damage} damage.")
                    player.mana -= skill_cost[spell]
            elif move == "Attack":
                player_damage = weapons[player.curr_weapon]
                print(f"\nYou used {move}, it does {player_damage} damage.")
                monsterhp -= player_damage
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(8, 16)
            print(
                f"\nIt is now the {monster}'s turn.\nThe {monster} attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
            if player.health < 0:
                break
        elif player.p_class == "Rogue":
            print("Do you want to [Attack], use a [Skill], or use a [Potion]")
            move = input("> ").title()
            if move == "Skill":
                print(player.skills)
                skill = rogue_input()
                if skill in player.skills:
                    player_damage = skill_damage[skill]
                    monsterhp -= player_damage
                    print(f"You used {skill}, it does {player_damage} damage.")
                    player.mana -= skill_cost[skill]
            elif move == "Attack":
                player_damage = weapons[player.curr_weapon]
                print(f"\nYou used {move}, it does {player_damage} damage.")
                monsterhp -= player_damage
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(8,16)
            print(
                f"\nIt is now the {monster}'s turn.\nThe {monster} attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
    player.xp += 60
    player.gold += 250
    player.end='END'



def BossFight(player: Player) -> None:
    monsterhp = 150
    monster = "Giant Rat"
    while monsterhp > 0 and player.health > 0:
        print(f"Player Health: {player.health}")
        print(f"Player Mana: {player.mana}")
        print(f"Monster Health: {monsterhp}")
        if player.p_class == "Knight":
            move = input(
                "\nDo you want to [Attack], use a [Sword Skill], or use a [Potion]? "
            ).title()
            if move == "Sword Skill" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Sword Skill":
                print(player.skills)
                skill = sword_skill_input()
                if skill in player.skills:
                    player_damage = skill_damage[skill]
                    monsterhp -= player_damage
                    print(f"You used {skill}, it does {player_damage} damage.")
                    player.mana -= skill_cost[skill]
            elif move == "Attack":
                player_damage = weapons[player.curr_weapon]
                print(f"You used {move}, it does {player_damage} damage.")
                monsterhp -= player_damage
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(8, 16)
            print(
                f"\nIt is now the {monster}'s turn.\nThe {monster} attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
        elif player.p_class == "Mage":
            print("Do you want to [Attack], use a [Spell], or use a [Potion]")
            move = input("> ").title()
            if move == "Spell" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Spell":
                print(player.skills)
                spell = spell_input()
                if spell in player.skills:
                    player_damage = skill_damage[spell]
                    monsterhp -= player_damage
                    print(f"You used {spell}, it does {player_damage} damage.")
                    player.mana -= skill_cost[spell]
            elif move == "Attack":
                player_damage = weapons[player.curr_weapon]
                print(f"\nYou used {move}, it does {player_damage} damage.")
                monsterhp -= player_damage
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(8, 16)
            print(
                f"\nIt is now the {monster}'s turn.\nThe {monster} attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
            if player.health < 0:
                break
        elif player.p_class == "Rogue":
            print("Do you want to [Attack], use a [Skill], or use a [Potion]")
            move = input("> ").title()
            if move == "Skill":
                print(player.skills)
                skill = rogue_input()
                if skill in player.skills:
                    player_damage = skill_damage[skill]
                    monsterhp -= player_damage
                    print(f"You used {skill}, it does {player_damage} damage.")
                    player.mana -= skill_cost[skill]
            elif move == "Attack":
                player_damage = weapons[player.curr_weapon]
                print(f"\nYou used {move}, it does {player_damage} damage.")
                monsterhp -= player_damage
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(8,16)
            print(
                f"\nIt is now the {monster}'s turn.\nThe {monster} attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
    player.xp += 40
    player.gold += 180

def skeletonfight(player: Player) -> None:
    print("As you go to take the gold, a skeleton jumps out and attacks!")
    monsterhp = 60
    monster = "Skeleton"
    while monsterhp > 0 and player.health > 0:
        print(f"Player Health: {player.health}")
        print(f"Player Mana: {player.mana}")
        print(f"{monster} Health: {monsterhp}")
        if player.p_class == "Knight":
            move = input(
                "\nDo you want to [Attack], use a [Sword Skill], or use a [Potion]? "
            ).title()
            if move == "Sword Skill" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Sword Skill":
                print(player.skills)
                skill = sword_skill_input()
                if skill in player.skills:
                    roll = random.randint(1,10)
                    hit = roll
                    if hit != 3 or hit != 7:
                        player_damage = skill_damage[skill]
                        monsterhp -= player_damage
                        print(f"You used {skill}, it does {player_damage} damage.")
                        player.mana -= skill_cost[skill]
                    else:
                        print("You missed!")
                        player.mana -= skill_cost[skill]
            elif move == "Attack":
                roll = random.randint(1,10)
                hit = roll
                if hit != 3 or hit != 7:
                    player_damage = weapons[player.curr_weapon]
                    print(f"You used {move}, it does {player_damage} damage.")
                    monsterhp -= player_damage
                else:
                    print("You missed!")
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(1, 8)
            print(
                f"\nIt is now the monster's turn.\nThe monster attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
        elif player.p_class == "Mage":
            print("Do you want to [Attack], use a [Spell], or use a [Potion]")
            move = input("> ").title()
            if move == "Spell" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Spell":
                print(player.skills)
                spell = spell_input()
                if spell in player.skills:
                    if player.mana < skill_cost[spell]:
                        print("You have no mana and failed to attack!")
                    else:
                        roll = random.randint(1,10)
                        hit = roll
                        if hit != 3 or hit != 7:
                            player_damage = skill_damage[spell]
                            monsterhp -= player_damage
                            print(f"You used {spell}, it does {player_damage} damage.")
                            player.mana -= skill_cost[spell]
                        else:
                            print("\nYou missed!")
                            player.mana -= skill_cost[spell]
            elif move == "Attack":
                roll = random.randint(1,10)
                hit = roll
                if hit != 3 or hit != 7:
                    player_damage = weapons[player.curr_weapon]
                    print(f"\nYou used {move}, it does {player_damage} damage.")
                    monsterhp -= player_damage
                else:
                    print("\nYou missed!")
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(1, 8)
            print(
                f"\nIt is now the monster's turn.\nThe monster attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
            if player.health < 0:
                break
        elif player.p_class == "Rogue":
            print("Do you want to [Attack], use a [Skill], or use a [Potion]")
            move = input("> ").title()
            if move == "Skill":
                print(player.skills)
                skill = rogue_input()
                if skill in player.skills:
                    roll = random.randint(1,10)
                    hit = roll
                    if hit != 3 or hit != 7:
                        player_damage = skill_damage[skill]
                        monsterhp -= player_damage
                        print(f"You used {skill}, it does {player_damage} damage.")
                        player.mana -= skill_cost[skill]
                    else:
                        print("You missed!")
                        player.mana -= skill_cost[skill]
            elif move == "Attack":
                roll = random.randint(1,10)
                hit = roll
                if hit != 3 or hit != 7:
                    player_damage = weapons[player.curr_weapon]
                    print(f"\nYou used {move}, it does {player_damage} damage.")
                    monsterhp -= player_damage
                else:
                    print("You missed!")
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(1, 8)
            print(
                f"\nIt is now the monster's turn.\nThe monster attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
    player.xp += 15
    player.gold += 30

def BossDun(player: Player, location: str) -> None:
    location='Entrance'
    print(BossDungeonMvmt["Entrance"])
    while player.health > 0:
        if location == "Exit":
            location == "Forrest2"
            break
        else:
            goto = input("> ").title()
            if (location, goto) in Boss_val:
                location = goto
                if location=='Exit':
                    location=="Forrest1"
                    break
                elif location == "Chasm":
                    print(BossDungeonMvmt['Chasm'])
                    DragonFight(player)
                    break
                else:
                    print(BossDungeonMvmt[goto])
            
            else:
                print("You cannot go there.")

def DreadTun(player: Player, location: str) -> None:
    location='Entrance'
    print(dreadfull_tunn_des["Entrance"])
    while player.health > 0:
        if location == "Exit":
            location == "Dreaded Tunnels"
            break
        else:
            goto = input("> ").title()
            if (location, goto) in dreadfull_tunnels:
                location = goto
                print(dreadfull_tunn_des[goto])
                if random_encounter():
                    combat(player)
                elif location == "Room4":
                    print(dreadfull_tunn_des["Room4"])
                    act = input("Do you want to take the gold? [Y/N]\n> ").title()
                    if act == "Y":
                        skeletonfight(player)
                        if player.health <= 0:
                            break
                        else:
                            player.gold += 125
                elif location == "BossRoom":
                    BossFight(player)
                    player.orb += 1
            else:
                print("You cannot go there.")


def mov_val(location: str, goto: str) -> bool:
    return (location, goto) in mvmt


def move(location: str, player: Player) -> str:
    while True:
        goto = input("Where would you like to go?> ").title()
        if location == "Dreadful Tunnels" and goto == "Entrance":
            DreadTun(player, location)
        elif goto=="Forrest2" and player.orb==1:
            location='Crypt of the Conquered King'
            print(towns['Crypt of the Conquered King'])
            BossDun(player, location)
            break
        elif location=="Forrest2" and goto == "Entrance":
            BossDun(player, location)
            break
        elif goto == "Forrest1" or goto == "Forrest3":
            if mov_val(location, goto):
                forrest1 = random.randint(1, 4)
                forrest3 = random.randint(1, 4)
                if goto == "Forrest1":
                    location = goto
                    print(forrest[forrest1])
                    break

                else:
                    location = goto
                    print(forrest[forrest3])
                    break

        elif (location == "Road1" or location == "Road3") and mov_val(location, goto):
            if goto == "Road2":
                print(towns[goto])
                location = goto
                break
            elif location == "Road1" and goto == player.sideloc:
                print(towns[goto])
                location = goto
                break
            else:
                if player.sideloc == "Waverly":
                    if goto == "Kingston" or goto == "Oakland":
                        location = goto
                        player.sideloc=goto
                        print(towns[goto])
                        break
                    else:
                        print(
                            f"You cannot goto {goto} from {location} coming from {player.sideloc}"
                        )
                        break
                elif player.sideloc == "Oakland":
                    if goto == "Riverside" or goto == "Waverly":
                        location = goto
                        player.sideloc=goto
                        print(towns[goto])
                        break
                    else:
                        print(
                            f"You cannot goto {goto} from {location} coming from {player.sideloc}"
                        )
                        break
                elif player.sideloc == "Riverside":
                    if goto == "Kingston" or goto == "Oakland":
                        location = goto
                        player.sideloc=goto
                        print(towns[goto])
                        break
                    else:
                        print(
                            f"You cannot goto {goto} from {location} coming from {player.sideloc}"
                        )
                        break
                else:
                    if goto == "Riverside" or goto == "Waverly":
                        location = goto
                        player.sideloc=goto
                        print(towns[goto])
                        break
                    else:
                        print(
                            f"You cannot goto {goto} from {location} coming from {player.sideloc}"
                        )
                        break
        elif mov_val(location, goto):
            location = goto
            print(towns[goto])
            break
        else:
            print(f"You cannot goto {goto} from {location}.")
            break
    return location

def level_up(player: Player) -> None:
    player.level += 1
    player.max_health += 25
    player.max_mana += 25
    player.health = player.max_health
    player.mana = player.max_mana
    player.xp -= 100
    print("You have leveled up! Congratulations!")
    print(f"Player Level: {player.level}")
    print(f"Max Health: {player.max_health}")
    print(f"Max Mana: {player.max_mana}")

def char_create(player: Player) -> None:
    while True:
        player.inventory = ["Rusted Sword", "God Sword"]
        print("Please create your character.")
        player.name = input("Name: ")
        player.p_class = input("Pick Mage, Knight, or Rogue: ").title()
        ()
        if player.p_class == "Mage":
            player.health = 60
            player.mana = 100
            player.max_health = 60
            player.max_mana = 100
            player.skills = ["Fireball", "Lunar Tempest", "Soul Rain"]
            break
        elif player.p_class == "Knight":
            player.health = 100
            player.mana = 60
            player.max_health = 100
            player.max_mana = 60
            player.skills = ["Vertical Arc", "Howling Octave", "Deadly Sins"]
            break
        elif player.p_class == "Rogue":
            player.health = 75
            player.mana = 75
            player.max_health = 75
            player.max_mana = 75
            player.skills = ["Long Shot", "Sneak Attack", "Sinister Strike"]
            break
        else:
            print("That is not a valid input")


def random_encounter() -> bool:
    encounter = random.randint(1, 5)
    if encounter == 1 or encounter == 2:
        return True
    else:
        return False


def random_mon() -> int:
    monster = random.randint(1, 4)
    return monster


def spell_input() -> str:
    spell = input("What spell do you want to cast? >").title()
    return spell


def rogue_input() -> str:
    skill = input("What skill do you want to use? >").title()
    return skill


def sword_skill_input() -> str:
    skill = input("Which sword skill would you like to use? ").title()
    return skill

def promotion(player: Player) -> None:
    print("You have reached level 10! You can now pick an advanced class.")
    if player.p_class == "Knight":
        print("As a Knight, you can go into Paladin or Barbarian. As a Barbarian, you lose mana and gain an enourmous amount of health. As a Paladin, you get a decent amount of both.")
        while True:
            act = input("Which one do you want? > ").title()
            if act == "Barbarian":
                player.max_health += 160
                player.max_mana -= 40
                player.advanced_class = "Barbarian"
                player.health = player.max_health
                player.mana = player.max_mana
                player.level += 1
                break
            elif act == "Paladin":
                player.max_health += 60
                player.max_mana += 60
                player.advanced_class = "Paladin"
                player.health = player.max_health
                player.mana = player.max_mana
                player.level += 1
                break
    elif player.p_class == "Mage":
        print("As a Mage, you can go into Grandmaster or Battlemage. As a Grandmaster, you gain a lot of mana but gain a slight amount of health. As a Battlemage, you get a decent amount of both.")
        while True:
            act = input("Which one do you want? > ").title()
            if act == "Grandmaster":
                player.max_health += 20
                player.max_mana += 100
                player.advanced_class = "Grandmaster"
                player.health = player.max_health
                player.mana = player.max_mana
                player.level += 1
                break
            elif act == "Battlemage":
                player.max_health += 60
                player.max_mana += 60
                player.advanced_class = "Battlemage"
                player.health = player.max_health
                player.mana = player.max_mana
                player.level += 1
                break
    else:
        print("As a Rogue, you can go into Assassin or Pirate. As an Assassin, you gain a moderate amount of health and mana. As a Pirate, you gain a good amount of health and a slight amount of mana.")
        while True:
            act = input("Which one do you want? > ").title()
            if act == "Assassin":
                player.max_health += 60
                player.max_mana += 60
                player.advanced_class = "Assassin"
                player.health = player.max_health
                player.mana = player.max_mana
                player.level += 1
                break
            elif act == "Pirate":
                player.max_health += 80
                player.max_mana += 40
                player.advanced_class = "Pirate"
                player.health = player.max_health
                player.mana = player.max_mana
                player.level += 1
                break


def combat(player: Player) -> None:
    random_mon()
    monsterhp = 70
    mon = random_mon()
    if mon == 1:
        monster = "slime"
    elif mon == 2:
        monster = "goblin"
    elif mon == 3:
        monster = "skeleton"
    elif mon == 4:
        monster = "bandit"
    print(f"You are fighting a {monster}")
    while monsterhp > 0 and player.health > 0:
        print(f"Player Health: {player.health}")
        print(f"Player Mana: {player.mana}")
        print(f"{monster} Health: {monsterhp}")
        if player.p_class == "Knight":
            move = input(
                "\nDo you want to [Attack], use a [Sword Skill], or use a [Potion]? "
            ).title()
            if move == "Sword Skill" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Sword Skill":
                print(player.skills)
                skill = sword_skill_input()
                if skill in player.skills:
                    roll = random.randint(1,10)
                    hit = roll
                    if hit != 3 or hit != 7:
                        player_damage = skill_damage[skill]
                        monsterhp -= player_damage
                        print(f"You used {skill}, it does {player_damage} damage.")
                        player.mana -= skill_cost[skill]
                    else:
                        print("You missed!")
                        player.mana -= skill_cost[skill]
            elif move == "Attack":
                roll = random.randint(1,10)
                hit = roll
                if hit != 3 or hit != 7:
                    player_damage = weapons[player.curr_weapon]
                    print(f"You used {move}, it does {player_damage} damage.")
                    monsterhp -= player_damage
                else:
                    print("You missed!")
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(1, 8)
            print(
                f"\nIt is now the monster's turn.\nThe monster attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
        elif player.p_class == "Mage":
            print("Do you want to [Attack], use a [Spell], or use a [Potion]")
            move = input("> ").title()
            if move == "Spell" and player.mana <= 4:
                print("\nYou have no mana and failed to attack!")
            elif move == "Spell":
                print(player.skills)
                spell = spell_input()
                if spell in player.skills:
                    if player.mana < skill_cost[spell]:
                        print("You have no mana and failed to attack!")
                    else:
                        roll = random.randint(1,10)
                        hit = roll
                        if hit != 3 or hit != 7:
                            player_damage = skill_damage[spell]
                            monsterhp -= player_damage
                            print(f"You used {spell}, it does {player_damage} damage.")
                            player.mana -= skill_cost[spell]
                        else:
                            print("\nYou missed!")
                            player.mana -= skill_cost[spell]
            elif move == "Attack":
                roll = random.randint(1,10)
                hit = roll
                if hit != 3 or hit != 7:
                    player_damage = weapons[player.curr_weapon]
                    print(f"\nYou used {move}, it does {player_damage} damage.")
                    monsterhp -= player_damage
                else:
                    print("\nYou missed!")
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(1, 8)
            print(
                f"\nIt is now the monster's turn.\nThe monster attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
            if player.health < 0:
                break
        elif player.p_class == "Rogue":
            print("Do you want to [Attack], use a [Skill], or use a [Potion]")
            move = input("> ").title()
            if move == "Skill":
                print(player.skills)
                skill = rogue_input()
                if skill in player.skills:
                    roll = random.randint(1,10)
                    hit = roll
                    if hit != 3 or hit != 7:
                        player_damage = skill_damage[skill]
                        monsterhp -= player_damage
                        print(f"You used {skill}, it does {player_damage} damage.")
                        player.mana -= skill_cost[skill]
                    else:
                        print("You missed!")
                        player.mana -= skill_cost[skill]
            elif move == "Attack":
                roll = random.randint(1,10)
                hit = roll
                if hit != 3 or hit != 7:
                    player_damage = weapons[player.curr_weapon]
                    print(f"\nYou used {move}, it does {player_damage} damage.")
                    monsterhp -= player_damage
                else:
                    print("You missed!")
            elif move == "Potion":
                use_potion(player)
            else:
                print("This action is unavailable!")
            enemy_damage = random.randint(1, 8)
            print(
                f"\nIt is now the monster's turn.\nThe monster attacks. It does {enemy_damage} damage.\n"
            )
            player.health = player.health - enemy_damage
    player.xp += 15
    player.gold += 70



def use_inventory(player: Player) -> None:
    print("\nThis is your inventory and stats.")
    print(f"Player Health: {player.health}")
    print(f"Player mana: {player.mana}")
    print(f"Player Level: {player.level}")
    print(f"Player XP: {player.xp}")
    print(f"Player Gold: {player.gold}")
    print(f"Health Potion: {player.health_potion}")
    print(f"Mana Potions: {player.mana_potion}")
    for item in player.inventory:
        print(f"{item}: {weapons[item]}")
    print(f"You are currently using a {player.curr_weapon}")
    action = input("Do you want to [Equip] or go [Back]? ").title()
    if action == "Equip":
        equip = input("What do you want to equip? ").title()
        if equip in player.inventory:
            player.curr_weapon = equip
        elif equip == player.curr_weapon:
            print("You are already using this weapon.")
        else:
            print("You do not have this item.")
    elif action == "Back":
        return
    else:
        print("Not Valid")


start_location = "Oakland"


def main():
    location = start_location
    player = Player("", 100, 100, 100, 100, "", "", 1, 0, 99999, 1, "God Sword", 10, 10, [], [], 'Oakland', '')
    while True:
        start = input("Would you like to start a [New Game] or [Load]? ").title()
        if start == "New Game":
            char_create(player)
            break
        elif start == "Load":
            load = input("Player name: ")
            try:
                with open(f"{load}/player_data.txt", "rb") as file:
                    player = pickle.load(file)
                with open(f"{load}/location.txt", "rb") as file:
                    location = pickle.load(file)
                break
            except FileNotFoundError:
                print("There is not a save for this person.")
    if location == "Forrest1" or location == "Forrest3":
        a=(1,2,3,4)
        loc=choice(a)
        print(forrest[loc])
    else:
        print(towns[location])
    while player.health > 0:
        if player.end=='END':
            print('You won the game!')
            break
        print("What would you like to do?")
        if (
            location == "Waverly"
            or location == "Riverside"
            or location == "Oakland"
            or location == "Kingston"
        ):
            act = input("[Move], [Inventory], [Potion], [Save], [Shop], [Quit]\n> ").title()
        else:
            act = input("[Move], [Inventory], [Potion], [Save], [Quit]\n> ").title()
        if act == "Inventory":
            use_inventory(player)
        elif act == "Potion":
            use_potion(player)
        elif player.xp >= 100:
            level_up(player)
        elif player.level == 10:
            promotion(player)
        elif act == "Add Level":
            player.level += 1
        elif act == "Save":
            try:
                os.mkdir(player.name)
            except FileExistsError:
                pass
            with open(f"{player.name}/player_data.txt", "wb") as file:
                pickle.dump(player, file)
            with open(f"{player.name}/location.txt", "wb") as file:
                pickle.dump(location, file)
        elif act == "Move":
            location = move(location, player)
            if random_encounter():
                combat(player)
        elif player.health <= 0:
            print("You have died.")
        else:
            print("You cannot do that.")


if __name__ == "__main__":
    main()
