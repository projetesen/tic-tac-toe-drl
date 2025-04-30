import numpy as np
import gym
from gym import spaces
import random
import matplotlib.pyplot as plt
 # <-- Modifie l'importation

# Définition de l'environnement personnalisé
class TicTacToeEnv(gym.Env):
    def __init__(self):
        super(TicTacToeEnv, self).__init__()
        self.action_space = spaces.Discrete(9)  # 9 cases possibles
        self.observation_space = spaces.Box(low=0, high=2, shape=(9,), dtype=np.int8)  # 0=vide, 1=joueur 1, 2=joueur 2
        self.state = np.zeros(9, dtype=np.int8)
        self.done = False
        self.current_player = 1

    def reset(self):
        self.state = np.zeros(9, dtype=np.int8)
        self.done = False
        self.current_player = 1
        return self.state

    def step(self, action):
        reward = 0
        if self.done or self.state[action] != 0:
            # Coup invalide
            reward = -10
            self.done = True
            return self.state, reward, self.done, {}

        self.state[action] = self.current_player

        if self.check_win(self.current_player):
            reward = 1
            self.done = True
        elif 0 not in self.state:
            reward = 0.5  # match nul
            self.done = True
        else:
            reward = 0
            self.current_player = 2 if self.current_player == 1 else 1  # changer de joueur

        return self.state, reward, self.done, {}

    def render(self):
        symbols = [' ', 'X', 'O']
        print('-------------')
        for i in range(3):
            print('|', symbols[self.state[3*i]], '|', symbols[self.state[3*i+1]], '|', symbols[self.state[3*i+2]], '|')
            print('-------------')

    def check_win(self, player):
        s = self.state
        win_states = [
            [s[0], s[1], s[2]],
            [s[3], s[4], s[5]],
            [s[6], s[7], s[8]],
            [s[0], s[3], s[6]],
            [s[1], s[4], s[7]],
            [s[2], s[5], s[8]],
            [s[0], s[4], s[8]],
            [s[2], s[4], s[6]],
        ]
        return any(all(cell == player for cell in line) for line in win_states)

# Correction ici ✅
def encode_state(state):
    """Convertir un état (9 cases) en un nombre pour indexer la Q-table"""
    num = 0
    state = state.astype(np.int32)  # Ajouté pour éviter OverflowError
    for i in range(9):
        num += state[i] * (3**i)
    return num

# Fonction de lissage (moyenne mobile)
def moving_average(data, window_size):
    """Appliquer une moyenne mobile pour lisser les données"""
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Paramètres
episodes = 1000
learning_rate = 0.1
discount_factor = 0.95
epsilon = 1.0
epsilon_decay = 0.995
epsilon_min = 0.01

env = TicTacToeEnv()
q_table = np.zeros((3**9, 9))  # 3^9 états possibles, 9 actions

rewards = []

# Entraînement
for episode in range(episodes):
    state = env.reset()
    total_reward = 0

    while True:
        state_encoded = encode_state(state)
        
        if random.uniform(0,1) < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(q_table[state_encoded])

        next_state, reward, done, _ = env.step(action)
        next_state_encoded = encode_state(next_state)

        # Update Q-table
        q_table[state_encoded, action] += learning_rate * (reward + discount_factor * np.max(q_table[next_state_encoded]) - q_table[state_encoded, action])

        total_reward += reward
        state = next_state

        if done:
            break

    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    rewards.append(total_reward)

    if (episode+1) % 100 == 0:
        print(f"Épisode {episode+1}/{episodes} - Récompense: {total_reward}")

# Lisser les récompenses avec une moyenne mobile
smoothed_rewards = moving_average(rewards, window_size=50)

# Affichage de la courbe d'apprentissage lissée
plt.plot(smoothed_rewards)
plt.xlabel('Épisode')
plt.ylabel('Récompense')
plt.title('Apprentissage de l\'agent Tic Tac Toe (Lissée)')
plt.grid()
plt.show()
from stable_baselines3 import PPO  # ou DQN selon ton choix
from stable_baselines3.common.vec_env import DummyVecEnv


# Environnement : envelopper dans un vecteur pour Stable-Baselines3
env = DummyVecEnv([lambda: TicTacToeEnv()])

# Créer et entraîner le modèle avec PPO (ou DQN)
model = PPO("MlpPolicy", env, verbose=1)  # Utilisation de MlpPolicy pour un réseau de neurones simple
# Si tu veux utiliser DQN, remplace PPO par DQN : model = DQN("MlpPolicy", env, verbose=1)

# Entraînement
model.learn(total_timesteps=100000)

# Sauvegarder le modèle
model.save("tic_tac_toe_model")

