from os import kill
from unicodedata import name
import pygame
from datatypes import *
import os
def clear():
    os.system('clear')
user = input("Enter username: ")
ip = "192.168.1.105"#input("Enter server ip: ")
port = 9000 #int(input("Enter server port: "))

connectionHandler = ConnectionHandler(ip,port,user)

gameobjecttypes = {
    'GameObject':GameObject,
    'Player': Player,
    'Bullet': Bullet
    }

#Start Pygame
pygame.init()
#Create the screen
screen=pygame.display.set_mode((800,600))
#Title
pygame.display.set_caption("War of Spaceships")
#Player
def render(gameObject):
    for data_to_render in gameObject.render():
        screen.blit(*data_to_render)

def render_game_objects(gameobjects):
    for gameObject in list(gameobjects.values()):
        render(gameObject)

def update_game_objects(gameobjects):
    gameobjects_to_delete = []
    for gO in gameobjects:
        if gameobjects[gO].update():
            gameobjects_to_delete.append(gO)
    for gO in gameobjects_to_delete:
        delete_game_object(gameobjects,gO)

def delete_game_object(gameobjects,oid):
    gameobject = gameobjects.pop(oid)
    del gameobject

#Game Loop
running = True

player = Player(300,400,0,user,"player.png")

scoreboard = Scoreboard(48,10)

gameobjects = {player.oid: player, scoreboard.oid: scoreboard}
object_counter = 2

bg = pygame.image.load("bg.jpeg")
connectionHandler.request("CONNECT")
while running:
    #time.sleep(0.2)

    screen.blit(bg, (0, 0))

    game_state_updates = connectionHandler.request("GET")
    new_game_objects_list = game_state_updates["gameobjects"]
    killcounts = game_state_updates["killcounts"]
    gameobjects["scoreboard"].killcounts = killcounts

    if new_game_objects_list:
        for gameObject in new_game_objects_list:
            if gameObject["oid"] in new_game_objects_list:
                gameobjects[gameObject["oid"]].x = gameObject["x"]
                gameobjects[gameObject["oid"]].y = gameObject["y"]
                gameobjects[gameObject["oid"]].w = gameObject["w"]
            else:
                dtype = gameObject.pop('dtype')
                gameobjects[gameObject["oid"]] = gameobjecttypes[dtype](*gameObject.values())
                object_counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == 'a':
                player.angular_velocity_ = -2
            if chr(event.key) == 'd':
                player.angular_velocity_ = +2
            if chr(event.key) == 's':
                player.velocity_ = -3
            if chr(event.key) == 'w':
                player.velocity_ = 3
            if event.key == 32:
                object_counter += 1
                bullet_oid = user + "-" + str(object_counter)

                bullet = player.shoot(bullet_oid)
                gameobjects[bullet.oid] = bullet

                connectionHandler.request("POST",[bullet.hashmap()])

        if event.type == pygame.KEYUP:
            if chr(event.key) == 'a':
                player.angular_velocity_ = 0
            if chr(event.key) == 'd':
                player.angular_velocity_ = 0
            if chr(event.key) == 's':
                player.velocity_ = 0
            if chr(event.key) == 'w':
                player.velocity_ = 0
            if event.key == 32:
                pass
    
    update_game_objects(gameobjects)
    for gameobject in gameobjects:
        if isinstance(gameobjects[gameobject],Bullet):
            if(user not in gameobjects[gameobject].oid):
                collide = player.rect_.colliderect(gameobjects[gameobject].rect_)
                if collide:
                    player.killer = gameobjects[gameobject].oid.split("-")[0]
                    delete_game_object(gameobjects,gameobject)
                    connectionHandler.request("POST",[player.hashmap()])
                    player.respawn()
                    break
                else:
                    pass
    connectionHandler.request("POST",[player.hashmap()])
    render_game_objects(gameobjects)

    pygame.display.update()

    #check for collisions
    """player_rect = pygame.Rect(player.x,player.y,50,50)
    for gameobject in gameobjects:
        if isinstance(gameobjects[gameobject],Bullet) and (user not in gameobjects[gameobject].oid):
            bullet_rect = pygame.Rect(gameobjects[gameobject].x,gameobjects[gameobject].y,50,50)
            collide = bullet_rect.colliderect(player_rect)
            if collide:
                player.killer = gameobjects[gameobject].oid.split("-")[0]
                delete_game_object(gameobjects,gameobject)
                connectionHandler.request("POST",[player.hashmap()])
                player.respawn()
                break
            else:
                pass"""
    
   
    
