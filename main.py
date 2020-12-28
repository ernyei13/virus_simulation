import pygame
import math
import random
import time
import numpy as np
import objects as ob
import stati as st
import logging
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_SPACE
)



infected = (212, 40, 66)
healthy = (49, 187, 73)
immune = (100, 50, 200)
dead = (0, 0, 0)

pygame.init()

screenwidth = 1200
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))
logging.basicConfig(filename='data.log', level=logging.DEBUG)
logging.debug("hello")

#INPUT DATA

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 10)

num_of_sector = 16

with open("in.txt", "r") as data:
    data = data.read().strip().splitlines()

for i in data:
    if i.split()[0] == "golyo:":
        num_of_dots = int(i.split()[1])
    if i.split()[0] == "meret:":
        ball_rad = int(i.split()[1])
    if i.split()[0] == "curve:":
        if i.split()[1] == "n":
            curv = False
        elif i.split()[1] == "y":
            curv = True
    if i.split()[0] == "ChanceOfInf:":
        ChanceOfInf = i.split()[1]
    if i.split()[0] == "linese:":
        if i.split()[1] == "n":
            linese = False
        elif i.split()[1] == "y":
            linese = True
    if i.split()[0] == "linese:":
        if i.split()[1] == "n":
            inputData = False
        elif i.split()[1] == "y":
            inputData = True
    if i.split()[0] == "fps:":
        if i.split()[1] == "n":
            fps = False
        elif i.split()[1] == "y":
            fps = True

#logfile inputnak

#space megallit +

#átlagsebesség számolás, csökken-e

#alapesetek, kapuk

#halál, gyogyul

#otthonmarad nyugszik





class Main():
    def __init__(self):
        self.runing = True
        self.time = 0
        self.list_of_lines = [ob.Object.Line(0, 0, healthy, screenwidth, 0), ob.Object.Line(screenwidth-2, 0, healthy, screenwidth-2, screenheight), ob.Object.Line(0, screenheight-2, healthy, screenwidth, screenheight-2), ob.Object.Line(0, 0, healthy, 0, screenheight+2)]

        self.list_of_dots = [ob.Object.Ball(screenwidth/2, screenheight/2, infected, ball_rad)]
        gridx = screenwidth // num_of_dots**(1/2)
        gridy = screenheight // num_of_dots**(1/2)
        for n in range(int(num_of_dots**(1/2))):
            for j in range(int(num_of_dots**(1/2))):
                self.list_of_dots.append(ob.Object.Ball(n*gridx + gridx // 2, j*gridy + gridy // 2, healthy, ball_rad))
        
        
        self.stat = st.Stat(self.list_of_dots)

        self.linemake = []

        self.list_of_objects = [[]]
        for i in range(num_of_sector):
            self.list_of_objects[0].append([])
            for j in range(num_of_sector):
                self.list_of_objects[0][i].append([])
        self.list_of_objects.append([])



    def update_list(self):
        self.list_of_objects = [[]]
        for i in range(num_of_sector):
            self.list_of_objects[0].append([])
            for j in range(num_of_sector):
                self.list_of_objects[0][i].append([])
        self.list_of_objects.append([])

        self.list_of_objects[1] = self.list_of_lines

        for i in self.list_of_dots:
            if i.x > screenwidth/2:
                if i.x > (screenwidth/4)*3:
                    if i.x > (screenwidth/8)*7:
                        col = 7
                    else:
                        col = 6
                else:
                    if i.x > (screenwidth/8)*5:
                        col = 5
                    else:
                        col = 4
            else:
                if i.x > screenwidth/4:
                    if i.x > (screenwidth/8)*3:
                        col = 3
                    else:
                        col = 2
                else:
                    if i.x > screenwidth/8:
                        col = 1
                    else:
                        col = 0

            if i.y > screenheight/2:
                if i.y > (screenheight/4)*3:
                    if i.y > (screenheight/8)*7:
                        row = 7
                    else:
                        row = 6
                else:
                    if i.y > (screenheight/8)*5:
                        row = 5
                    else:
                        row = 4
            else:
                if i.y > screenheight/4:
                    if i.y > (screenheight/8)*3:
                        row = 3
                    else:
                        row = 2
                else:
                    if i.y > screenheight/8:
                        row = 1
                    else:
                        row = 0

            self.list_of_objects[0][row][col].append(i)



    def makeline(self):
        if len(self.linemake) == 2:
            if abs(self.linemake[0][0] - self.linemake[1][0]) >= abs(self.linemake[0][1] - self.linemake[1][1]):
                self.list_of_lines.append(ob.Object.Line(self.linemake[0][0], self.linemake[0][1], healthy, self.linemake[1][0], self.linemake[0][1]))
                self.linemake = []
            else:
                self.list_of_lines.append(ob.Object.Line(self.linemake[0][0], self.linemake[0][1], healthy, self.linemake[0][0], self.linemake[1][1]))
                self.linemake = []



    def run(self):
        stop = True
        fps = 0

        font = pygame.font.Font('freesansbold.ttf', 32)
           

        while self.run:
            fps += 1
            start_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN: #gotta make clean
                    self.linemake.append([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
                    self.makeline()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        if stop == True:
                            stop = False
                        elif stop == False:
                            stop = True

            screen.fill((200,100,180))


            if curv == True and stop == False:
                self.stat.update(screenwidth)

                for i in self.stat.ret():
                    pygame.draw.line(screen, (0,0,0), (i[0][0]-self.time, i[0][1]), (i[1][0]-self.time, i[1][1]), 1)

            self.update_list()

            for i in range(len(self.list_of_objects[0])):
                for j in range(len(self.list_of_objects[0][i])):
                    try:

                        korul = [[*self.list_of_objects[0][i-1][j-1], *self.list_of_objects[0][i][j-1], *self.list_of_objects[0][i+1][j-1],
                             *self.list_of_objects[0][i-1][j], *self.list_of_objects[0][i][j], *self.list_of_objects[0][i+1][j],
                             *self.list_of_objects[0][i-1][j+1], *self.list_of_objects[0][i][j+1], *self.list_of_objects[0][i+1][j+1]], self.list_of_objects[1]]
                    except:
                        if i < len(self.list_of_objects[0])-1 and j < len(self.list_of_objects[0])-1:
                            if i == 0 and j != 0:
                                korul = [[ *self.list_of_objects[0][i][j-1], *self.list_of_objects[0][i+1][j-1],
                                     *self.list_of_objects[0][i][j], *self.list_of_objects[0][i+1][j],
                                      *self.list_of_objects[0][i][j+1], *self.list_of_objects[0][i+1][j+1]], self.list_of_objects[1]]

                            if i != 0 and j == 0:
                                korul = [[
                                     *self.list_of_objects[0][i-1][j], *self.list_of_objects[0][i][j], *self.list_of_objects[0][i+1][j],
                                     *self.list_of_objects[0][i-1][j+1], *self.list_of_objects[0][i][j+1], *self.list_of_objects[0][i+1][j+1]], self.list_of_objects[1]]

                        if i > 0 and j > 0:
                            if i == len(self.list_of_objects[0])-1 and j != len(self.list_of_objects[0])-1:
                                korul = [[*self.list_of_objects[0][i-1][j-1], *self.list_of_objects[0][i][j-1], 
                                     *self.list_of_objects[0][i-1][j], *self.list_of_objects[0][i][j], 
                                     *self.list_of_objects[0][i-1][j+1], *self.list_of_objects[0][i][j+1]], self.list_of_objects[1]]

                            if i != len(self.list_of_objects[0])-1 and j == len(self.list_of_objects[0])-1:
                                korul = [[*self.list_of_objects[0][i-1][j-1], *self.list_of_objects[0][i][j-1], *self.list_of_objects[0][i+1][j-1],
                                     *self.list_of_objects[0][i-1][j], *self.list_of_objects[0][i][j], *self.list_of_objects[0][i+1][j]
                                     ], self.list_of_objects[1]]

                    finally:
                        if [i,j] == [0,0]:
                            korul = [[
                                  *self.list_of_objects[0][i][j], *self.list_of_objects[0][i+1][j],
                                 *self.list_of_objects[0][i][j+1], *self.list_of_objects[0][i+1][j+1]], self.list_of_objects[1]]

                        if [i,j] == [0,len(self.list_of_objects[0])-1]:
                            korul = [[ *self.list_of_objects[0][i][j-1], *self.list_of_objects[0][i+1][j-1],
                                *self.list_of_objects[0][i][j], *self.list_of_objects[0][i+1][j]],
                                 self.list_of_objects[1]]


                        if [i,j] == [len(self.list_of_objects[0])-1,0]:
                             korul = [[
                                 *self.list_of_objects[0][i-1][j], *self.list_of_objects[0][i][j],
                                 *self.list_of_objects[0][i-1][j+1], *self.list_of_objects[0][i][j+1]], self.list_of_objects[1]]

                        if [i,j] == [len(self.list_of_objects[0])-1, len(self.list_of_objects[0])-1]:
                             korul = [[*self.list_of_objects[0][i-1][j-1], *self.list_of_objects[0][i][j-1],
                                 *self.list_of_objects[0][i-1][j], *self.list_of_objects[0][i][j],
                                 ], self.list_of_objects[1]]



                    
                    for o in self.list_of_objects[0][i][j]:
                        o.collision_detect(korul)
                        o.draw(screen)
                        if stop == True:
                            continue
                        o.move()

                        #print(o)
                        #if self.time == 0 or self.time > 1000:
                        #    print(o.speed)
                        #    print("-----")
                        if linese == True:
                            for k in o.lines:
                                if o.color == infected and k.color == infected:
                                    pygame.draw.line(screen, (255,250,250), (o.x, o.y), (k.x, k.y), 1)


            for n in self.list_of_lines:
                n.optimize()
                n.draw(screen)

            if stop == False:
                self.time += 0.5

            
            text = font.render("FPS: {}".format(round(1.0 / (time.time() - start_time))), True, (2,50,150))
            screen.blit(text, (0,0))

            pygame.display.flip()


game = Main()
game.run()

