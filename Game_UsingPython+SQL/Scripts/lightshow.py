# import pygame

from Scripts.obstacles import PreLazer
from random import randint

class LightShow:
    def __init__(self, game, surf):
        self.game = game
        self.surf = surf
        
        self.cooldown = 0.5
        self.currentTime = 0.0
        
        self.orientations = ['Horizontal-L', 'Vertical-L']
        
        # PreLazer(self.game, self.orientations[randint(0,1)], randint(0,self.game.ScreenSize[1]), 20, self.surf)
        
        self.a = [
            'PreLazer(self.game, self.orientations[0], 0, 40, self.surf)',
            'PreLazer(self.game, self.orientations[0], (self.game.ScreenSize[1] * 0.25), 40, self.surf)',
            'PreLazer(self.game, self.orientations[0], (self.game.ScreenSize[1] * 0.5), 40, self.surf)',
            'PreLazer(self.game, self.orientations[0], (self.game.ScreenSize[1] * 0.75), 40, self.surf)',
            'PreLazer(self.game, self.orientations[0], self.game.ScreenSize[1], 20, self.surf)'
        ]
        
        self.n = 0

    def update(self, dt):
        if self.currentTime >= self.cooldown:
            # eval(self.a[self.n])
            # self.n += 1
            # if self.n > len(self.a) - 1:
            #     self.n = 0
            self.Random()
            self.currentTime = 0.0
        else:
            self.currentTime += dt
            
        self.game.preLazerGroup.update(dt)
        self.game.preLazerGroup.draw(self.surf)
        
        self.game.LazerGroup.update(dt)
        self.game.LazerGroup.draw(self.surf)
        
    def Random(self):
        rand = randint(0,1)
        PreLazer(self.game, self.orientations[rand], randint(0,self.game.ScreenSize[rand]), 20, self.surf)