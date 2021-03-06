import time
from abc import abstractmethod
from random import choice
from twitchbot import The_Castle_Game


attributes_list = ['walls', 'moat', 'bridge', 'archers']
sqlite_file = r'MyFiles\ViewerData.sqlite'

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
            'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

names = ['bob', 'joe', 'smith', 'wow', 'kappa', 'ron', 'gotdott', 'popbob', 'manoli', 'thukor', 'paincakes', 'hlr']


class Viewer:
    def __init__(self, username, UID, points):
        self.username = username
        self.UID = UID
        self.points = points
        self.playerside = 0

    def username(self):
        self.username = ''
        self.UID = ''


class Castle:
    def __init__(self, castle_name, walls, moat, bridge, archers):
        self.castle_name = castle_name
        self.walls = walls
        self.moat = moat
        self.bridge = bridge
        self.archers = archers

    def castle_name(self):
        self.castle_name = ''

    def points(self):
        points = self.points
        return points

    def walls(self):
        walls = self.points
        return walls

    def moat(self):
        moat = self.points
        return moat


class Unit_Properties:
    def __init__(self, health, armor, melee, ranged, movespeed, experience):
        self.health = health
        self.armor = armor
        self.melee = melee
        self.ranged = ranged
        self.movespeed = movespeed
        self.experience = experience

    @abstractmethod
    def unittype(self):
        """Return a string representing the type of unit this is"""
        pass


class Archer:
    def __init__(self, name):
        self.unittype = "Bow and arrow user, faster than melee units"
        self.health = 25
        self.armor = 2
        self.ranged = 10
        self.movespeed = 2

        self.name = name

        self.maplocation = ""
        self.unitdistanceplaceholder = 0


class Calvalry:
    def __init__(self, name):
        self.unittype = "Horse and rider, very fast"
        self.health = 35
        self.armor = 5
        self.melee = 5
        self.movespeed = 5

        self.name = name

        self.maplocation = ""
        self.unitdistanceplaceholder = 0


class Swordsmen:
    def __init__(self, name):
        self.unittype = "Slower soldier, heavily armored and good at melee"
        self.health = 50
        self.armor = 15
        self.melee = 15
        self.movespeed = 1

        self.name = name

        self.maplocation = ""
        self.unitdistanceplaceholder = 0


class Spy:
    def __init__(self, name):
        self.unittype = "Used for subtlety, good for collecting information on opponents"
        self.health = 5
        self.armor = 1
        self.melee = 10
        self.ranged = 10
        self.movespeed = 3

        self.name = name

        self.maplocation = ""
        self.unitdistanceplaceholder = 0


class warmap:
    def __init__(self, rangecount):
        self.boardplaces = []
        self.rangecount = rangecount
        self.player1side = 1
        self.player2side = 2

    def boardmap(self):
        for num in range(self.rangecount):
            for j in alphabet:
                self.boardplaces.append(j+str(num+1))
        return self.boardplaces

    def mapmovement(self, unit):
        currlocation = list(unit.maplocation)
        unit.maplocation = str(currlocation[0]) + str(int(currlocation[1] + 1))  # moves forward from a1 to a2


class timer:
    def __init__(self):
        self.timerstart = time.time()
        self.timerend = time.time()
        self.counter = 0


def layout1():
    layer1 = "xxxxx"
    layer2 = layer1
    layer3 = "yyyyy"
    layer4 = layer3
    layer5 = layer3
    return [layer1, layer2, layer3, layer4, layer5]


def movement():
    ourhorse = Calvalry(name="horsey")
    oursoldier = Swordsmen(name="soldier")

    ourmap = warmap(rangecount=200)

    movementtimer = timer()
    movestart = movementtimer.timerstart
    movecount = movementtimer.counter

    engagetimer = timer()
    engagestart = engagetimer.timerstart

    while True:
        moveend = time.time()
        move_difference = moveend - movestart
        if move_difference >= 1:
            ourhorse.unitdistanceplaceholder = abs(ourhorse.unitdistanceplaceholder + ourhorse.movespeed +
                                                   ourmap.rangecount)
            oursoldier.unitdistanceplaceholder = abs(oursoldier.movespeed * movecount - ourmap.rangecount)
            print("Ourhorse has moved this far total", str(ourhorse.unitdistanceplaceholder) + ", on this turn:",
                  movecount)
            print("Oursoldier has moved this far total", str(oursoldier.unitdistanceplaceholder) + ", on this turn:",
                  movecount)
            print('\n')
            movestart = time.time()
            movecount += 1
            if ourhorse.unitdistanceplaceholder >= oursoldier.unitdistanceplaceholder:
                print('Forces have met on turn', movecount)
                break
    while True:
        engageend = time.time()
        engage_diff = engageend - engagestart
        if engage_diff >= 1:
            engagement(ourhorse, oursoldier)
            engagement(oursoldier, ourhorse)
            movecount += 1
            printedengage = engagementprinted(ourhorse, oursoldier, movecount)
            engagestart = time.time()
            if printedengage is False:
                break
            if printedengage is False:
                break


def engagement(unit1, unit2):
    if unit1.armor > 0:
        unit1.armor = unit1.armor - unit2.melee
    elif unit1.armor == 0:
        unit1.health = unit1.health - unit2.melee
    elif unit1.armor < 0:
        unit1.health = unit1.health - abs(unit1.armor)
        unit1.armor = 0


def engagementprinted(unit1, unit2, counter):
    if unit1.health <= 0 and unit2.health <= 0:
        print("Both units were killed in action")
        print('\n')
        return False
    elif unit1.health <= 0:
        print(unit2.name, "wins and has", unit2.armor, "armor remaining and", unit2.health, "health remaining")
        print('\n')
        return False
    elif unit2.health <= 0:
        print(unit1, "wins and has", unit1.armor, "armor remaining and", unit1.health, " health remaining")
        print('\n')
        return False
    else:
        print('On turn:', counter)
        print(unit2.name, "has", unit2.armor, "armor left and", unit2.health, "health remaining")
        print(unit1.name, "has", unit1.armor, "armor left and", unit1.health, "health remaining")
        print('\n')


def testpopulate(whichside):
    testlayout = layout1()
    layercount = 0  # determines which layer we are on
    startinglocationcount = 1  # this is incremented to give each soldier their own number on their line, a1 vs a2
    listiter = testlayout[-1 - layercount]
    unitlist = []

    current_letter = ""
    current_lettercount = ""
    if whichside == 1:
        current_lettercount = 0  # determines which letter we are on starting at A, other side starts at Z
        current_letter = alphabet[current_lettercount]  # slices our alphabet list at current letter

    elif whichside == 2:
        current_lettercount = 25
        current_letter = alphabet[current_lettercount]

    for layer in testlayout:
        breakstring = list(listiter)
        for letterinlayer in breakstring:
            startinglocation = 13 - (int(len(breakstring) / 2) + (len(breakstring) % 2 > 0)) + startinglocationcount
            if letterinlayer == 'y':
                newarcher = Archer(name=choice(names))
                newarcher.maplocation = str(current_letter) + str(startinglocation)
                unitlist.append(newarcher)
                startinglocationcount += 1
            if letterinlayer == 'x':
                newsword = Swordsmen(name=choice(names))
                newsword.maplocation = str(current_letter) + str(startinglocation)
                unitlist.append(newsword)
                startinglocationcount += 1
        startinglocationcount = 1
        if whichside == 1:
            current_lettercount += 1
        if whichside == 2:
            current_lettercount -= 1
        current_letter = alphabet[current_lettercount]
        layercount += 1
        if layercount+1 > len(testlayout):
            break
        else:
            listiter = testlayout[-1-layercount]

    return unitlist


def main():
    unit1 = Swordsmen("bob")
    unit2 = Calvalry("horsey")

    movement()
    #engagementprinted(counter=10, unit1=unit1, unit2=unit2)
    # engagementprinted(counter=10, unit1=soldier)
    # testpopulate(whichside=2)


main()

"""
get the length of each row, find the middle of it, and create a way for the middle unit to be on 13

int(len(breakstring)/2) + (len(breakstring)%2 > 0)
startinglocation = 13 - int(len(breakstring)/2) + (len(breakstring)%2 > 0) + 1
create a count which starts at 1 then goes up until that row is done
Need a way to determine which row to start on - depending on side start at A or Z
Need to assign each player a side at start of fight - should be in warmap class(?)
big if loop which checks player side, if side 1 start A and iterate forwards if side 2 do inverse


rows can only be odd numbers
create a max number of rows you can have (25?)
"""


"""
How to define war? two forces meet. 
One force chooses to assault second force either
    a. in transit (scouted with spies or army)
        1. can happen across this on accident 
            * two forces in motion on different task and one changes priorities
                (second force should have reduced efficieny by like 5%-15%)
            or
        2. spend resources searching for opponents and if found send out your army
    b. at base
        1. second force chooses to meet on open field
        2. force stays at home and becomes part of castle defense (army is x% less effective 
            due to being stuck inside)
        3. force leaves base (if possible) and attempts to assault from side (expand upon this later)


How do fights happen?
Movespeed
- Time based, armies start x seconds apart and meet in the middle
    - Archers can engage at x seconds
    - Swordsmen can engage at x seconds
    - Calvalry can engage at x seconds
- Design different formations, some formations stronger than others
How to design each type of attack/defense?

Make preset options for war such as:
    -If no response-
    Choose to fight/ignore
    If attacked run/stand and fight
Make preset options for how to fight:
    Calvalry engages after swordsmen
    Calvalry attempts to go around
    Expand on this
"""


