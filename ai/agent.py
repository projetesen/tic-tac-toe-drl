from stable_baselines3 import PPO  # ou DQN selon ton modèle
import numpy as np
from ai.train import TicTacToeEnv

  # Assurez-vous d'importer l'environnement

class Agent:
    def __init__(self, model_path="tic_tac_toe_model"):
        # Charger le modèle préalablement sauvegardé
        self.model = PPO.load(model_path)  # ou DQN.load(model_path)
    
    def play(self, state):
        """Faire jouer l'agent dans un état donné"""
        action, _states = self.model.predict(state)  # Prédire l'action à partir de l'état
        return action

    def reset(self):
        """Réinitialiser l'agent si nécessaire"""
        pass

# Utilisation
if __name__ == "__main__":
    agent = Agent(model_path="tic_tac_toe_model")
    env = TicTacToeEnv()

    state = env.reset()
    done = False
    while not done:
        action = agent.play(state)  # Obtenir l'action de l'agent
        state, reward, done, _ = env.step(action)  # Appliquer l'action et obtenir le nouveau state
        env.render()  # Afficher le jeu (optionnel)
