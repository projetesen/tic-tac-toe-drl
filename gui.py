import tkinter as tk
import socket
import threading
import numpy as np
from ai.agent import Agent

# Connexion au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))  # Modifie si nécessaire

# Charger l'agent IA
agent = Agent("ai/model.zip")

# Variables globales
current_player = "X"
board = np.zeros(9, dtype=int)
is_ai = tk.BooleanVar()

# Fonctions
def envoyer_action_au_serveur(action):
    try:
        client_socket.send(str(action).encode())
    except:
        print("Erreur d'envoi au serveur.")

def recevoir_du_serveur():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            traiter_reponse(data)
        except:
            break

def traiter_reponse(data):
    global board, current_player
    infos = data.split(",")
    action = int(infos[0])
    joueur = infos[1]

    board[action] = 1 if joueur == "X" else 2
    boutons[action]["text"] = joueur

    if joueur == current_player:
        status_label.config(text="C'est votre tour !")
        if is_ai.get() and current_player == "X":
            jouer_tour()
    else:
        status_label.config(text="Attente de l'adversaire...")

def cliquer_case(index):
    if board[index] == 0 and current_player == "X":
        envoyer_action_au_serveur(index)

def jouer_tour():
    if is_ai.get() and current_player == "X":
        action = agent.predict(board)
        envoyer_action_au_serveur(action)
    else:
        print("C'est au joueur humain de jouer.")

# Interface graphique
root = tk.Tk()
root.title("Tic Tac Toe - Réseau avec IA")

# Checkbox pour IA
ai_checkbox = tk.Checkbutton(root, text="Jouer avec IA", variable=is_ai)
ai_checkbox.pack()

# Label d'information
status_label = tk.Label(root, text="Attente de l'adversaire...", font=("Arial", 14))
status_label.pack()

# Grille de jeu
frame = tk.Frame(root)
frame.pack()

boutons = []
for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 32), width=5, height=2,
                    command=lambda i=i: cliquer_case(i))
    btn.grid(row=i//3, column=i%3)
    boutons.append(btn)

# Thread pour recevoir du serveur
threading.Thread(target=recevoir_du_serveur, daemon=True).start()

# Lancement de la fenêtre
root.mainloop()



