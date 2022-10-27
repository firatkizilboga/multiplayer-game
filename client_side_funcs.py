import socket
from datatypes import Package
def GET(name,ip,port):
    p=Package(name,"GET",0,0)
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.connect((ip, port))
    cmd = f'{p.to_json()} \r\n\r\n'.encode()
    mysock.send(cmd)
    package_list = []
    while True:
        data = mysock.recv(512)
        if len(data) < 1:
            break
        data = data.decode()
        print(data)
        return Package.read_json(data)

def POST(name,ip,port,x,y):
    p=Package(name,"POST",x,y)
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.connect((ip, port))
    cmd = f'{p.to_json()} \r\n\r\n'.encode()
    mysock.send(cmd)
    while True:
        data = mysock.recv(512)
        if len(data) < 1:
            break
        print(data.decode(),end='')
    mysock.close()
    