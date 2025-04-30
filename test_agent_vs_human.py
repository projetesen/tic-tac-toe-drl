from ai.agent import Agent
from ai.train import TicTacToeEnv  # Cette fois, ça doit fonctionner


env = TicTacToeEnv()
agent = Agent("ai/tic_tac_toe_model.zip")

state = env.reset()
done = False

while not done:
    env.render()
    if env.current_player == 1:  # IA joue (tu peux adapter selon ton implémentation)
        action = agent.play(state)
        print(f"L'IA joue : {action}")
    else:
        action = int(input("Ton tour (0-8) : "))

    state, reward, done, _ = env.step(action)

env.render()
if reward == 1:
    print("L'IA a gagné !")
elif reward == -1:
    print("Tu as gagné !")
else:
    print("Match nul.")

