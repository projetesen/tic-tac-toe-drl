# === IMPORTS ===
import socket

# === PARAMÈTRES DU CLIENT ===
HOST = '127.0.0.1'  # Adresse du serveur (localhost pour un test local)
PORT = 12345        # Port sur lequel le serveur écoute

# === CRÉATION DU SOCKET CLIENT ===
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
client_socket.connect((HOST, PORT))

# Fonction pour recevoir les messages du serveur
def recevoir_message():
    while True:
        try:
            msg = client_socket.recv(1024).decode()  # Recevoir le message
            if msg:
                print(msg)
            else:
                break
        except:
            break

# Démarrer un thread pour recevoir les messages en continu
import threading
thread_recevoir = threading.Thread(target=recevoir_message)
thread_recevoir.start()

# Envoi de messages au serveur
while True:
    message = input("Entrez votre message (ou 'exit' pour quitter) : ")
    if message.lower() == 'exit':
        break
    client_socket.send(message.encode())

# Fermer la connexion
client_socket.close()
