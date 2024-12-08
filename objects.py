import pygame
from utilitaires import *

class Object:
    pass

class Apple(Object):
    def __init__ (self, x, y):
        self.health = 5
        self.is_used = False
        self.x = x
        self.y = y
        self.type = 'apple'

class Chicken(Object):
    def __init__ (self, x, y):
        self.health = 10
        self.is_used = False
        self.x = x
        self.y = y
        self.type = 'chicken'
    
