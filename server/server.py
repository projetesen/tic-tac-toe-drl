# === IMPORTS ===
import socket
import threading

# === PARAMÈTRES DU SERVEUR ===
HOST = '127.0.0.1'  # Adresse du serveur (localhost)
PORT = 12345        # Port sur lequel le serveur écoute

# === CRÉATION DU SERVEUR SOCKET ===
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)  # Limité à 2 joueurs pour cette version

print(f"🎮 Serveur lancé sur {HOST}:{PORT} (attente des joueurs...)")

# Liste des clients connectés
clients = []

# === FONCTION POUR GÉRER LA COMMUNICATION AVEC UN CLIENT ===
def gerer_client(client_socket, adresse, joueur_id):
    # Envoie un message de bienvenue au joueur
    bienvenue_msg = f"Bienvenue Joueur {joueur_id} !\n"
    client_socket.send(bienvenue_msg.encode())
    print(f"Message envoyé à Joueur {joueur_id} : {bienvenue_msg}")

    
    while True:
        try:
            # Recevoir les messages du client
            msg = client_socket.recv(1024).decode()  # Taille du buffer : 1024 octets
            if msg:
                print(f"[Joueur {joueur_id}] {msg}")
                # Relayer le message à l'autre joueur
                for c in clients:
                    if c != client_socket:
                        c.send(f"Joueur {joueur_id} : {msg}".encode())
            else:
                break
        except:
            break

    print(f"❌ Joueur {joueur_id} déconnecté")
    clients.remove(client_socket)
    client_socket.close()

# === BOUCLE POUR ACCEPTER DEUX CLIENTS ===
joueur_id = 1
while len(clients) < 2:
    client, addr = server_socket.accept()
    print(f"✅ Connexion de {addr}")
    clients.append(client)
    thread = threading.Thread(target=gerer_client, args=(client, addr, joueur_id))
    thread.start()
    joueur_id += 1

print("🔒 Le serveur attend des messages des joueurs...")
input("Appuie sur Entrée pour quitter...")

