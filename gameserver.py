from socket import *
import json
import os
def clear():
    os.system('clear')

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    gameobjects = {}
    getters = {}
    killcounts = {}
    try :
        serversocket.bind(("localhost",9000))
        serversocket.listen()
        while(1):
            (clientsocket, address) = serversocket.accept()
            rd = clientsocket.recv(512*512).decode()
            pieces = rd.split("\n")
            hashmap = json.loads(pieces[0])
            user, r_type, data = hashmap["user"], hashmap["r_type"], hashmap["data"]
            if r_type == "POST":
                for gameobject in data:
                    if (gameobject["dtype"] == "Player"):
                        gameobjects[gameobject["oid"]] = gameobject
                        killer = gameobject["killer"]
                        if  killer is not None:
                            killer = gameobject["killer"]
                            if killer not in killcounts:
                                killcounts[killer] = 1
                            else:
                                killcounts[killer] += 1
                            print(killcounts)
                    if (gameobject["oid"] not in gameobjects) or (gameobject["dtype"] == "Player"):
                        gameobjects[gameobject["oid"]] = gameobject

            gameobjects_to_send = []
            if r_type == "CONNECT":
                max_getter = []
                for getter in getters:
                    len_getter = len(getters[getter])
                    if len_getter > len(max_getter):
                        max_getter = getters[getter]
                getters[user] = max_getter

            if r_type == "GET":
                if user not in getters:
                    getters[user] = []
                for go in gameobjects:
                    if user in go:
                        pass
                    elif gameobjects[go]["dtype"] == "Player":
                        gameobjects_to_send.append(gameobjects[go])
                    elif go in getters[user]:
                        pass
                    else:
                        gameobjects_to_send.append(gameobjects[go])
                        getters[user].append(go)
                hashmap = {
                    'user': 'server',
                    'r_type': 'game_state_updates',
                    'data': {"gameobjects": gameobjects_to_send, "killcounts": killcounts}
                }
                command = json.dumps(hashmap) + "\r\n\r\n"
                clientsocket.sendall(command.encode())
            clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n");
    
    """except Exception as exc :
        print("Error:\n");
        print(exc)"""

    serversocket.close()

#print(gethostbyname(gethostname()),gethostname(),9000)
print("run 'ngrok tcp 9000'")
createServer()