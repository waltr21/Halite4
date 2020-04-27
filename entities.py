class Ship:
    def __init__(self, id, x, y, friendly):
        self.id = id
        self.x = x
        self.y = y
        self.friendly = friendly
        self.halite = 0

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
        self.setSpaces(nums)
        self.numPlayers = numPlayers
        self.step = 0
        # self.show()

    def getHalite(self, x, y):
        return self.getSpace(x, y).halite

    def getSpace(self, x, y):
        # Flipped because.... arrays :|
        return self.spaces[y][x]

    def setShipSpace(self, ship):
        self.getSpace(ship.x, ship.y).ship = ship

    def getPlayer(self, id):
        for ship in self.allShips:
            if (ship.id == id):
                return ship
        return None

    def updateShip(self, ship, halite):
        cur = self.getPlayer(ship.id)
        cur.x = ship.x
        cur.y = ship.y
        cur.halite = halite

    def updatePlayers(self, obs):
        playerIndex = obs['player']
        allShipIds = obs['players'][playerIndex][2].keys()

        # Set friendly players on board.
        for id in allShipIds:
            player = obs['players'][playerIndex][2][id]
            # See if the ship exists in the game
            ship = self.getPlayer(id)

            if(ship is None):
                newShip = Ship(id, player[0] % 15, player[0] // 15, True)
                self.setShipSpace(newShip)
                self.allShips.append(newShip)
            else:
                self.updateShip(ship, player[1])

        # Set all other players
        for i in range(self.numPlayers):
            # Make sure we are not looking at own players
            if (i != playerIndex):
                allShipIds = obs['players'][i][2].keys()
                # Set friendly players on board.
                for id in allShipIds:
                    player = obs['players'][i][2][id]
                    # See if the ship exists in the game
                    ship = self.getPlayer(id)

                    if(ship is None):
                        newShip = Ship(id, player[0] % 15, player[0] // 15, False)
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
        countX = 0
        countY = 0
        for num in nums:
            if (countX == 15):
                countX = 0
                countY += 1
            self.getSpace(countX, countY).halite = num
            countX += 1
    def getAction(self):
        return {}

    def show(self):
        for row in self.spaces:
            for space in row:
                if(space.ship is not None):
                    print(space.ship.id, end =" ")
                else:
                    print(space.halite, end =" ")
            print("")
