import pygame
import math
import random
import time
import numpy as np




infected = (212, 40, 66)
healthy = (49, 187, 73)
immune = (100, 50, 200)
dead = (0, 0, 0)


class Object():
    def __init__(self, type):
        self.type = ''

    class Ball():
        def __init__(self, x, y, color, rad):

            self.speed = np.array([[math.cos(math.radians(random.randint(0, 360)))],[math.sin(math.radians(random.randint(0, 360)))]])
            self.x = x
            self.y = y
            self.color = color
            self.type = 'Ball'
            self.radius = rad
            self.lines = [self]

        def __str__(self):    
            return "{} {}".format(self.speed[0][0], self.speed[1][0])
        
        def seb(self):
            return sqrt(self.speed[0][0]**2+self.speed[1][0]**2)

        
        def draw(self, screen):
            if np.isnan(self.x):
                self.x = 0
            if np.isnan(self.y):
                self.y = 0
            
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, 0)

        def move(self):
            self.x += self.speed[0][0]
            self.y += self.speed[1][0]
        
        def ChangeDirection(self, dot_2):
            vekt_regi = self.speed
            if np.isnan(self.x):
                self.x = int(0)
            if np.isnan(self.y):
                self.y = int(0)
            if np.isnan(dot_2.x):
                dot_2.x = int(0)
            if np.isnan(dot_2.y):
                dot_2.y = int(0)
        
            vc = np.array(self.x, self.y)
            vc1 = np.array(dot_2.x, dot_2.y)
            self.speed = self.speed -( np.dot((self.speed - dot_2.speed), (vc-vc1)) / (vc-vc1)**2) * (vc-vc1)
            dot_2.speed = dot_2.speed -( np.dot((dot_2.speed - vekt_regi), (vc1-vc)) / (vc1-vc)**2) * (vc1-vc)
        
        def ChangeDirection2(self, where):
            if where == "x":
                self.speed[0][0] = -self.speed[0][0]

            if where == "y":
                self.speed[1][0] = -self.speed[1][0]

            #print(self.speed)


        def collision_detect(self, list_of_dots):
            for i in list_of_dots[0]:
                if i.type == 'Ball':
                    #if i == self.lines[-1] or i.lines[-1] == self:
                    #    continue
                    distance_x = abs(self.x - i.x)
                    distance_y = abs(self.y - i.y)
                    if distance_x == 0 and distance_y == 0:
                        continue
                    
                    if distance_x**2 + distance_y**2 <= (2*self.radius)**2 and self.lines[-1] != i:
                            self.lines.append(i)
                            i.lines.append(self)
                            self.ChangeDirection(i)
                            self.infectin(i)
                            if len(self.lines) > 20:
                                self.lines = self.lines[0:10]
                            

            for i in list_of_dots[1]:
                if i.type == 'Line':
                    k_distance_x = abs(self.x - i.x)
                    k_distance_y = abs(self.y - i.y)
                    k_dist = math.sqrt(k_distance_x**2 + k_distance_y**2)

                    v_distance_x = abs(self.x - i.end_x)
                    v_distance_y = abs(self.y - i.end_y)
                    v_dist = math.sqrt(v_distance_x**2 + v_distance_y**2)



                    if k_distance_x <= self.radius and self.y > i.y-self.radius and self.y < i.end_y + self.radius and self.lines[-1] != i:
                        self.ChangeDirection2("x")
                        self.lines.append(i)
                    if k_distance_y <= self.radius and self.x > i.x-self.radius and self.x < i.end_x + self.radius and self.lines[-1] != i:
                        self.ChangeDirection2("y")
                        self.lines.append(i)

        def infectin(self, other_dot):
            if self.color == infected and other_dot.color == healthy:
                self.infect(other_dot)
            if self.color == healthy and other_dot.color == infected:
                self.infect(other_dot)

        def infect(self, other_dot):
            other_dot.color = infected
            self.color = infected


    class Line():
        def __init__(self, x, y, color, end_x, end_y):
            self.type = 'Line'
            self.x = x
            self.y = y
            self.color = color
            self.end_x = end_x
            self.end_y = end_y
            self.length = math.sqrt((end_x-x)**2+(end_y-y)**2)

        def optimize(self):
            if self.x > self.end_x:
                x = self.x
                self.x = self.end_x
                self.end_x = x
            if self.y > self.end_y:
                y = self.y
                self.y = self.end_y
                self.end_y = y

        def draw(self, screen):
            pygame.draw.line(screen, self.color,(self.x, self.y), (self.end_x, self.end_y), 2)

