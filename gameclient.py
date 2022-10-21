import pygame
import time
import client_side_funcs
from packagedatatypes import Package
name = input("Enter username: ")
ip = input("Enter server ip: ")
port = int(input("Enter server port: "))
#Start Pygame
pygame.init()

#Create the screen
screen=pygame.display.set_mode((800,600))

#Title
pygame.display.set_caption("Space Invaders")

#Player
playerImg = pygame.image.load('./player.png')
def player(x,y):
    screen.blit(playerImg,(x,y))
x=300
y=400
player_x_change = 0
player_y_change = 0

#Game Loop
running = True
while running:
    screen.fill((0,0,0))
    opponent = client_side_funcs.GET(name,ip,port)
    if opponent == "no opponent":
        pass
    else: 
        player(int(opponent.x),int(opponent.y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
            if chr(event.key) == 'a':
                player_x_change=-1
            if chr(event.key) == 'd':
                player_x_change=+1
            if chr(event.key) == 's':
                player_y_change=+1
            if chr(event.key) == 'w':
                player_y_change=-1
        if event.type == pygame.KEYUP:
            if chr(event.key) == 'a':
                player_x_change=0
            if chr(event.key) == 'd':
                player_x_change=0
            if chr(event.key) == 's':
                player_y_change=0
            if chr(event.key) == 'w':
                player_y_change=0

    x = x + player_x_change
    y = y + player_y_change
    client_side_funcs.POST(name,ip,port,x,y)
    player(x,y)
    pygame.display.update()
