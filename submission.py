from random import choice
from kaggle_environments import evaluate, make
from entities import Board, Ship, ShipYard, Space

board = None
numPlayers = 0

def setPlayers(obs):
    global numPlayers, board
    numPlayers = len(obs['players'])
    playerIndex = obs['player']
    allPlayerIds = obs['players'][playerIndex][2].keys()
    # Set friendly players on board.
    for id in allPlayerIds:
        player = obs['players'][playerIndex][2][id]
        tempShip = Ship(id, player[0] % 15, player[0] // 15, True)
        board.setShipSpace(tempShip)

    # Set all other players
    for i in range(numPlayers):
        # Make sure we are not looking at own players
        if (i != playerIndex):
            allPlayerIds = obs['players'][i][2].keys()
            # Set friendly players on board.
            for id in allPlayerIds:
                player = obs['players'][i][2][id]
                tempShip = Ship(id, player[0] % 15, player[0] // 15, False)
                board.setShipSpace(tempShip)

    board.show()

def start(obs):
    global board, numPlayers
    board = Board(obs['halite'])
    setPlayers(obs)
    board.updateHalite(obs['halite'])



def process(obs):
    action = {}
    ship_ids = list(obs.players[obs.player][2].keys())

    for ship_id in ship_ids:
        getAction(ship_id)
        decision = convert()
        ship_action = decision
        if ship_action is not None:
            action[ship_id] = decision

    # if(len(ship_ids)  == 0):
    #     action = spawn()


    return action

if __name__ == "__main__":
    env = make("halite", debug=True)
    trainer = env.train([None, "submission"])
    observation = trainer.reset()
    start(observation)
    env.render()

    while not env.done:
        #my_action = process(observation)
        my_action = {}
        # print("my action", my_action)
        observation, reward, done, info = trainer.step(my_action)
        # env.render(mode="ipython", width=100, height=90, header=False, controls=False)
    # env.render()
