import socket
from _thread import *
from game import Game
import pickle

# server script has to be running, on the right machine
server = "192.168.178.26"
port = 5555 # should be open usually

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

# this is for having unlimited number of games (with 2 players each...)
connected = set()
games = {}
idCount = 0



def threaded_client(conn, p, gameId):
    # threaded functions: running in the background, does not need to be finished for loop to continue
    # this is running for each client joining
    global idCount # if someone leaves, its still there
    conn.send(str.encode(str(p))) # we are telling them what player they area
    reply = ""
    while True:
        try:
            # here we send the options the players have
            data = conn.recv(4096).decode() # increase this number if necessary, this is to constantly receive string data from the client

            if gameId in games:
                # check if the game still exists
                game = games[gameId]

                if not data:
                    break
                else:
                    # here come the options
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        # then it must be a move which is in data
                        game.play(p, data)

                    reply = game
                    conn.sendall(pickle.dumps(reply))

            else:
                break
        except:
            break

    print("Lost Connection")
    try:
        del games[gameId] # delete the game
        print("Closing Game ", gameId)
    except:
        pass
    idCount =-1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount -1)//2 # for every two people who join; keeps track how many games we need
    if idCount % 2 == 1:
        # we need to create a new game, there is no pair
        games[gameId] = Game(gameId) # this initializes a new game
        print("Creating a new game...")

    else: # new person has to be become part of existing game
        games[gameId].ready = True
        p = 1 # player is 1

    #  now we start the thread
    start_new_thread(threaded_client, (conn, p, gameId))
