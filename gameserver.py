from socket import *
from packagedatatypes import Package

def createServer():
    serversocket = socket(AF_INET, SOCK_STREAM)
    player_objects = {}
    try :
        serversocket.bind(("192.168.1.106",9000))
        serversocket.listen(5)
        while(1):
            (clientsocket, address) = serversocket.accept()
            rd = clientsocket.recv(5000).decode()
            pieces = rd.split("\n")
            print(pieces)
            package = Package.read_json(pieces[0])
            if package.request == "POST":
                player_objects[package.name] = package
                clientsocket.shutdown(SHUT_WR)
            data = ""
            if package.request == "GET":
                for po in player_objects:
                    if po != package.name:
                        data = player_objects[po].to_json() + "\r\n\r\n"
                if data == "":
                    p=Package('','',1000,1000)
                    data = p.to_json() + "\r\n\r\n"
                clientsocket.sendall(data.encode())
                clientsocket.shutdown(SHUT_WR)

    except KeyboardInterrupt :
        print("\nShutting down...\n");
    #except Exception as exc :
    #    print("Error:\n");
    #    print(exc)

    serversocket.close()

print(gethostbyname(gethostname()),gethostname(),9000)
print("run 'ngrok tcp 9000'")
createServer()
