from random import randint
import logging


class Ship:
    def __init__(self, id, x, y, friendly):
        self.id = id
        self.x = x
        self.y = y
        self.friendly = friendly
        self.halite = 0
        self.target = (0,0)

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

    def getAction(self):
        return self.move(randint(1, 4))

class ShipYard:
    def __init__(self, id, x, y, friendly):
        self.id = id
        self.x = x
        self.y = y
        self.friendly = friendly

class Space:
    def __init__(self, x, y, amt):
        self.halite = amt
        self.x = x
        self.y = y
        self.ship = None
        self.shipYard = None

    def reset(self):
        self.halite = 0
        self.ship = None
        self.shipYard = None

    def show(self):
        print(str(str(self.halite) + " - " + str(self.x) + ", " + str(self.y)))

class Board:
    def __init__(self, nums, numPlayers):
        self.spaces = []
        self.allShips = []
        self.allShipYards = []
        self.setSpaces(nums)
        self.numPlayers = numPlayers
        self.step = 0
        self.myHalite = 0
        # self.show()

    def getHalite(self, x, y):
        return self.getSpace(x, y).halite

    def getSpace(self, x, y):
        # Flipped because.... arrays :|
        return self.spaces[y][x]

    def setShipSpace(self, ship):
        self.getSpace(ship.x, ship.y).ship = ship

    def setShipYardSpace(self, yard):
        self.getSpace(yard.x, yard.y).shipYard = yard

    def getShip(self, id):
        for ship in self.allShips:
            if (ship.id == id):
                return ship
        return None

    def getShipYard(self, id):
        for yard in self.allShipYards:
            if (yard.id == id):
                return yard
        return None

    def updateShip(self, ship, halite):
        cur = self.getShip(ship.id)
        cur.x = ship.x
        cur.y = ship.y
        cur.halite = halite
        #print("Updating: " + ship.id)

    def updateShipYards(self, obs):
        playerIndex = obs['player']
        allShipYardIds = obs['players'][playerIndex][1].keys()

        # Set all other players
        for i in range(self.numPlayers):
            # Make sure we are not looking at own players
            allShipYardIds = obs['players'][i][1].keys()
            # Set friendly players on board.
            for id in allShipYardIds:
                pos = obs['players'][i][1][id]
                # See if the ship exists in the game
                yard = self.getShipYard(id)

                if(yard is None):
                    newYard = None
                    if (i != playerIndex):
                        newYard = ShipYard(id, pos % 15, pos // 15, False)
                    else:
                        newYard = ShipYard(id, pos % 15, pos // 15, True)
                    self.setShipSpace(newYard)
                    self.allShipYards.append(newYard)

    def updatePlayers(self, obs):
        playerIndex = obs['player']
        allShipIds = obs['players'][playerIndex][2].keys()

        # Set all players
        for i in range(self.numPlayers):
            # Make sure we are not looking at own players

            allShipIds = obs['players'][i][2].keys()
            # Set friendly players on board.
            for id in allShipIds:
                player = obs['players'][i][2][id]
                # See if the ship exists in the game
                ship = self.getShip(id)

                if(ship is None):
                    newShip = None
                    if (i != playerIndex):
                        newShip = Ship(id, player[0] % 15, player[0] // 15, False)
                    else:
                        newShip = Ship(id, player[0] % 15, player[0] // 15, True)
                    self.setShipSpace(newShip)
                    self.allShips.append(newShip)
                else:
                    self.updateShip(ship, player[1])

        self.removeShips(obs)

    # Do not love this at the moment...
    def removeShips(self, obs):
        allIds = []
        for ship in self.allShips:
            allIds.append(ship.id)

        for i in range(self.numPlayers):
                allShipIds = obs['players'][i][2].keys()
                # Set friendly players on board.
                for id in allShipIds:
                    for temp in allIds:
                        if (id == temp):
                            allIds.remove(temp)
        #print(allIds)
        # All ids is now a list of ids to remove?
        for id in allIds:
            for ship in self.allShips:
                if (id == ship.id):
                    self.allShips.remove(ship)

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
        logging.info('This is an info message')
        countX = 0
        countY = 0
        for num in nums:
            if (countX == 15):
                countX = 0
                countY += 1
            self.getSpace(countX, countY).halite = num
            self.getSpace(countX, countY).ship = None
            countX += 1

    def getAction(self):
        action = {}
        friends = self.getFriendlyShips()
        yards = self.getFriendlyShipYards()
        if (self.step == 1 and len(friends) > 0):
            action[friends[0].id] = "CONVERT"
            return action
        if(len(yards) > 0 and self.myHalite >= 2000):
            if(self.getSpace(yards[0].x, yards[0].y).ship is None):
                action[yards[0].id] = "SPAWN"
                return action
        for ship in friends:
            action[ship.id] = ship.getAction()

        return action

    def getFriendlyShips(self):
        temp = []
        for ship in self.allShips:
            if (ship.friendly):
                temp.append(ship)
        return temp

    def getFriendlyShipYards(self):
        temp = []
        for yard in self.allShipYards:
            if (yard.friendly):
                temp.append(yard)
        return temp

    def show(self):
        for row in self.spaces:
            for space in row:
                if(space.ship is not None):
                    print(space.ship.id, end =" ")
                else:
                    print(space.halite, end =" ")
            print("")

    def showInfo(self):
        for ship in self.allShips:
            print( ship.id + ' - ' + str(ship.x) + ',' + str(ship.y))
