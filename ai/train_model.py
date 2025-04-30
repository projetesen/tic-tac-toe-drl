from stable_baselines3 import PPO  # ou DQN selon ton choix
from ai.train import TicTacToeEnv  # Assure-toi d'avoir l'environnement TicTacToe

# Créer l'environnement
env = TicTacToeEnv()

# Créer le modèle PPO (ou DQN)
model = PPO("MlpPolicy", env, verbose=1)

# Entraîner le modèle
model.learn(total_timesteps=10000)  # Tu peux augmenter ce nombre pour un entraînement plus long

# Sauvegarder le modèle
model.save("ai/tic_tac_toe_model")
