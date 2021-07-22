# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
Created on Thu Jul 22 12:22:06 2021

@author: Lorenzo Signoretti
"""


from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import question
import time
from random import randint


def accept_in_connections():
    """This function accept entry connection """
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è collegato." % client_address)

        #information about the game
        msg_client('Benvenuto!', client)
        msg_client('Rispondi più velocemente possibile alle domande', client)
        msg_client('Chi ha il punteggio più alto alla fine del tempo, vince!', client)
        
        
        #Dictionary for client
        address[client] = client_address
        #Thread - one for each client
        Thread(target=manage_client, args=(client,)).start()
        

def manage_client(client):
    """Manage the single clinet connection"""
    #information about the player
    msg_client('Ora inserisci il tuo nome: ', client)
    name = client.recv(BUFSIZ)
    clients[client] = name
    
    init_player(client)
    
    #get player's role
    msg_client('Il tuo ruolo è: ' + str(roles[client]), client)
    msg_client('Scrivi {quit} per uscire dal gioco', client)
    
    insert_number_player(client)
    
    start_question(client)
    
    check_player_ready(client)
    
    start_game(client)
    
    search_winner()
    
    close_client(client)
    

def broadcast(msg):
    """Send a message to each client"""
    for user in clients:
        msg_client(msg, user)

def msg_client(msg, client):
    """Simple function to sent message to client"""
    client.send(bytes(str(msg), "utf-8"))

#=====================================================
def init_player(client):
    """Initialize the player"""
    roles[client] = question.random_role()
    score[client] = 0
    
def insert_number_player(client):
    """The first player can choose the number of player for the match"""
    global num_player
    global player_insert
    if player_insert == False:
        msg_client('Inserire il numero di giocatori: ', client)
        msg = client.recv(BUFSIZ)
        check_quit(msg, client)
        num_player = check_number(client, msg, 1, nPlayer)
        
        player_insert = True

def start_question(client):
    """Ask to client to choose a number, if this is the random trap number the player loses the game """
    global num_player
    
    # Select option trap
    trap = randint(min_start, max_start)
    # Ask for the option
    msg_client("Hai " + str(max_start) + " scelte, scegli attentamente ", client)
    msg_client("Scrivi un numero compreso tra " + str(min_start) + " e " + str(max_start) + ": ", client)
    msg = client.recv(BUFSIZ)
    # Check if is {quit}
    check_quit(msg, client)
    # Check if it's between of min number and max number
    answer = check_number(client, msg, min_start, max_start)
    # Check if he choose the trap
    if answer == trap:
        msg_client("Scelta sbagliata, sarà per la prossima volta! ", client)
        if num_player > 1:
            num_player -= 1
        close_client(client)
    else:
        msg_client("Perfetto, ora hai la possibilità di confrontarti con gli giocatori", client)
        
def start_game(client):
    """Main function of the game. Send qustion to player and check the answer"""
    Thread(target=countdown, args=(play_time, client)).start()
    max_question = game_max_question
    number_question = 0
    
    msg_client("ATTENZIONE: Tutte le risposte vanno inserite con la lettera maiuscola!", client)
    
    while number_question != max_question and gameover == False:
        # Take random question, send to client and wait for answer
        random_question, correct_answer= choose_question()
        msg_client(random_question, client)
        answer = client.recv(BUFSIZ)
        check_quit(answer, client)
        # Check if is correct and add score
        if answer == bytes(str(correct_answer), "utf8"):
            msg_client('Risposta corretta! Hai guadagnato un punto', client)
            score[client] += 1
        else :
            msg_client('Risposta errata! Hai perso un punto', client)
            score[client] -= 1
        number_question += 1

def search_winner():
    """Detrminate the winner"""
    global max_player_name
    global gameover
    max_score = -5
    draw = False
    gameover = True
    # Find Max score
    for client in score:
        if max_score < score[client]:
            max_score = score[client]
            max_player_name = clients[client] 
            draw = False
        elif max_score == score[client] and len(score) != 1:
            draw = True
    if draw:
        broadcast(bytes("La partita è finita in pareggio", "utf8"))
    else:
        broadcast(bytes("Il vincitore è : " + max_player_name + " con " + str(max_score) + " punti!", "utf8"))
#=====================================================
def check_number(client, num, min, max):
    """Cast a string to a number and check if this is in the correct range"""
    while True:
        try:
            # Convert it into integer
            temp = int(num)
            if temp >= min and temp <= max:
                break
            else:
                msg_client(client, "Perfavore, inserire un numero compreso tra: " + str(min) + " e " + str(max) + ": ")
                num= client.recv(BUFSIZ)
        except ValueError:
            msg_client(client, "Perfavore, inserire un numero compreso tra: " + str(min) + " e " + str(max) + ": ")
            num = client.recv(BUFSIZ)              
    return temp

def check_quit(string, client):
    """Check if the string is equal to {quit}"""
    if string == bytes("{quit}", "utf8"):
        close_client(client)

def check_player_ready(client):
    while len(clients) != num_player:
        if len(clients) < num_player:
            msg_client("In attesa degli altri giocatori", client)
        else:   
            msg_client("Troppi giocatori, qualcuno lasci la chat per continuare", client)
        time.sleep(5)  
    msg_client("Comincia il gioco, in bocca al lupo!", client)

#=====================================================
def countdown(timer, client):
    """A simpple timer. At the end gameover switch to true"""
    global gameover
    while timer :
        time.sleep(1)
        timer -= 1
    gameover = True
    
def choose_question():
    """Choose a random answer"""
    random_index_question = randint(1, question.num_question + 1)
    random_question = question.question[random_index_question]
    correct_answer = question.answer[random_index_question]
    return random_question, correct_answer

def close_client(client):
    """Close client and print to all that user left the chat
    """
    client.close()
    broadcast(bytes("%s ha abbandonato" % clients[client], "utf8"))
    del clients[client]
    del roles[client]
    del score[client]
    del address[client]

#====================================================    
clients = {}    #Save player's name
address = {}    #Save player's address
roles = {}      #Save player's role
score = {}      #Save player's score


gameover = False#game state, when it's True the game finish
nPlayer = 5
min_start = 1   #Min number to choose in start question
max_start = 3   #Max number to choose in start question
game_max_question = 5
play_time = 50  #Timer 

player_insert = False
num_player = 1
max_player_name = "null"

HOST = ''
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("In attesa di connessioni...")
    ACCEPT_THREAD = Thread(target=accept_in_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
