import json
import socket
import pygame
import math
class ConnectionHandler:
    def __init__(self,ip,port,user) -> None:
        self.ip,self.port,self.user = ip, port, user
    def request(self,r_type,data=None):
        hashmap = {
            'user': self.user,
            'r_type': r_type,
            'data': data
        }
        command = json.dumps(hashmap) + "\r\n\r\n"
        mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mysock.connect((self.ip, self.port))
        mysock.send(command.encode())
        while True:
            data = mysock.recv(512*512)
            if len(data) < 1:
                break
            hashmap = data.decode()
            response = json.loads(hashmap)
            if r_type == "GET":
                response = response["data"]
            else:
                pass
            return response
    
class GameObject:
    def __init__(self,x,y,w,oid=None,img=None) -> None:
        self.x,self.y,self.w,self.oid,self.img = x,y,w,oid,img
        if img is not None:
            self.mask_ = pygame.image.load(self.img)
    def update(self):
        return False
    def render(self):
        return [[pygame.transform.rotate(self.mask_,-(self.w)),(self.x,self.y)]]
    def hashmap(self):
        hmap = dict()
        for key in self.__dict__:
            if "_" not in key:
                hmap[key] = self.__dict__[key]
        hmap["dtype"] = self.__class__.__name__
        return hmap
    
            
class Player(GameObject):
    def __init__(self, x, y, w, oid = None, img = None,killer=None):
        super().__init__(x,y,w,oid,img)
        self.velocity_ = 0
        self.angular_velocity_ = 0
        self.killer = killer
    def move(self):
        self.x += -self.velocity_*math.cos(math.radians(self.w))
        self.y += -self.velocity_*math.sin(math.radians(self.w))
    def rotate(self):
        self.w += self.angular_velocity_
    def update(self):
        self.move()
        self.rotate()
        self.rect_ = pygame.Surface.get_rect(self.mask_, center=(self.x, self.y))
        return False
    def shoot(self,oid):
        return Bullet(self.x,self.y,self.w,oid)
    def render(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render(self.oid, True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.x, self.y + 40)
        return [[pygame.transform.rotate(self.mask_,-(self.w)),(self.x,self.y)],[text,textRect]]
    def respawn(self):
        self.killer = None
        self.x, self.y, self.w, self.velocity_, self.angular_velocity_ = 400, 300, 0, 0, 0

class Bullet(GameObject):
    def __init__(self,x,y,w,oid=None,img='bullet.png'):
        super().__init__(x,y,w,oid,img)
        self.velocity_ = 4
        self.distance_ = 0
    def move(self):
            self.x += -self.velocity_*math.cos(math.radians(self.w))
            self.y += -self.velocity_*math.sin(math.radians(self.w))
            self.distance_ += self.velocity_
    def update(self):
        self.move()
        self.rect_ = pygame.Surface.get_rect(self.mask_, center=(self.x, self.y))
        if self.distance_ > 1000:
            return True
        else:
            return False

class Scoreboard(GameObject):
    def __init__(self,x,y) -> None:
        super().__init__(x,y,0,"scoreboard")
        self.killcounts = {}
    def render(self):
        texts_to_render = []
        font = pygame.font.Font('freesansbold.ttf', 16)
        text = font.render("scoreboard: ", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (self.x, self.y)
        texts_to_render.append([text,textRect])
        tmp_y = self.y + 20
        for player in self.killcounts:
            data = f"{player}: {self.killcounts[player]}"
            font = pygame.font.Font('freesansbold.ttf', 16)
            text = font.render(data, True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (self.x, tmp_y)
            texts_to_render.append([text,textRect])
            tmp_y += 20
        return texts_to_render
