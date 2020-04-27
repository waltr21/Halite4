from random import choice
from kaggle_environments import evaluate, make
from entities import Board, Ship, ShipYard, Space

board = None

def updateBoard(obs):
    global board
    # First step involves creating all objects.
    if (obs['step'] == 1):
        board = Board(obs['halite'], len(obs['players']))
        return

    board.step = obs['step']
    board.updateHalite(obs['halite'])
    board.updatePlayers(obs)

    # board.show()

def process(obs):
    updateBoard(obs)
    return board.getAction()

if __name__ == "__main__":
    env = make("halite", debug=True)
    trainer = env.train([None, "submission", "submission", "submission"])
    observation = trainer.reset()
    env.render()

    while not env.done:
        my_action = process(observation)
        # print("my action", my_action)
        observation, reward, done, info = trainer.step(my_action)
        # env.render(mode="ipython", width=100, height=90, header=False, controls=False)
    # env.render()
