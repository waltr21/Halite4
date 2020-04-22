class Ship:
    def __init__(self, id, x, y, friendly):
        self.id = id
        self.x = x
        self.y = y
        self.friendly = friendly

    def move(self, dir):
        if(dir == 1):
            return "NORTH"
        if(dir == 2):
            return "EAST"
        if(dir == 3):
            return "SOUTH"
        if(dir == 4):
            return "WEST"
        else:
            return None

    def spawn(self):
        return "SPAWN"

    def convert(self):
        return "CONVERT"

class ShipYard:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Space:
    def __init__(self, x, y, amt):
        self.halite = amt
        self.x = x
        self.y = y
        self.ship = None
        self.shipYard = None

    def show(self):
        print(str(str(self.halite) + " - " + str(self.x) + ", " + str(self.y)))

class Board:
    def __init__(self, nums):
        self.spaces = []
        self.setSpaces(nums)
        # self.show()

    def getHalite(self, x, y):
        return self.getSpace(x, y).halite

    def getSpace(self, x, y):
        # Flipped because.... arrays :|
        return self.spaces[y][x]

    def setShipSpace(self, ship):
        self.getSpace(ship.x, ship.y).ship = ship

    def setSpaces(self, nums):
        countX = 0
        countY = 0
        tempList = []
        for num in nums:
            if (countX == 15):
                self.spaces.append(tempList)
                tempList = []
                countX = 0
                countY += 1
            tempList.append(Space(countX, countY, num))
            countX += 1
        self.spaces.append(tempList)

    def updateHalite(self, nums):
        countX = 0
        countY = 0
        for num in nums:
            if (countX == 15):
                countX = 0
                countY += 1
            self.getSpace(countX, countY).halite = num
            countX += 1

    def show(self):
        for row in self.spaces:
            for space in row:
                if(space.ship is not None):
                    print(space.ship.id, end =" ")
                else:
                    print(space.halite, end =" ")
            print("")
