import pygame
import objects as ob

infected = (212, 40, 66)
healthy = (49, 187, 73)
immune = (100, 50, 200)
dead = (0, 0, 0)




class Stat():
    def __init__(self, list_of_dots):
        self.moment = 0
        self.graph = []
        self.list_of_dots = list_of_dots

    def update(self, scrlen):
        inf = 0
        for i in self.list_of_dots:
            if i.type == "Ball" and i.color == infected:
                inf += 1
        self.graph.append([[round(self.moment) + scrlen-20, 200],[round(self.moment)+scrlen-20, 200-(inf*(200/len(self.list_of_dots)))]])

        self.moment += 0.5

    def ret(self):
        return self.graph