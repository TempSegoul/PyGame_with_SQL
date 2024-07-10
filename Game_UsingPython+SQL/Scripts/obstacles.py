import pygame

class PreLazer(pygame.sprite.Sprite):
    def __init__(self, game, orientation, pos, thickness, surf):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.orientation = orientation
        self.pos = pos
        self.thickness = thickness
        
        self.currentThickness = 0.0
        
        self.surf = surf
        
        self.warmupTime = 1.0
        self.currentWarmupTime = 0.0
        
        match orientation:
            case 'Horizontal-L':
                self.image = pygame.Surface((self.game.ScreenSize[0], self.currentWarmupTime), pygame.SRCALPHA)
                self.image.fill((255, 0, 0, 50))
                self.rect = self.image.get_rect()
                self.rect.topleft = (0, self.pos)
            case 'Vertical-L':
                self.image = pygame.Surface((self.currentWarmupTime, self.game.ScreenSize[1]), pygame.SRCALPHA)
                self.image.fill((255, 0, 0, 50))
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos, 0)
            case _:
                print("HEH")
            
        self.game.preLazerGroup.add(self)
                  
    def update(self, dt=1):
        
        self.currentThickness = (self.currentWarmupTime / self.warmupTime) * self.thickness
        
        match self.orientation:
            case 'Horizontal-L':
                self.image = pygame.Surface((self.game.ScreenSize[0], self.currentThickness), pygame.SRCALPHA)
                self.image.fill((255, 0, 0, 50))
                self.rect = self.image.get_rect()
                self.rect.topleft = (0, self.pos-int(self.currentThickness*0.5))
            case 'Vertical-L':
                self.image = pygame.Surface((self.currentThickness, self.game.ScreenSize[1]), pygame.SRCALPHA)
                self.image.fill((255, 0, 0, 50))
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos-int(self.currentThickness*0.5), 0)
            case _:
                print("HEH")

        if self.currentWarmupTime < self.warmupTime:
            self.currentWarmupTime += dt
        else:
            self.InstantiateLazer()
            self.kill()
            
    def InstantiateLazer(self):
        match self.orientation:
            case 'Horizontal-L':
                self.image = pygame.Surface((self.game.ScreenSize[0], self.thickness), pygame.SRCALPHA)
                self.image.fill((255, 0, 0, 50))
                self.rect = self.image.get_rect()
                self.rect.topleft = (0, self.pos-int(self.currentThickness*0.5))
                Lazer(self.game, self.image, self.rect, self.rect.topleft, self.game.ScreenSize[0], self.thickness, self.orientation, self.surf)
            case 'Vertical-L':
                self.image = pygame.Surface((self.thickness, self.game.ScreenSize[1]), pygame.SRCALPHA)
                self.image.fill((255, 0, 0, 50))
                self.rect = self.image.get_rect()
                self.rect.topleft = (self.pos-int(self.currentThickness*0.5), 0)
                Lazer(self.game, self.image, self.rect, self.rect.topleft, self.game.ScreenSize[1], self.thickness, self.orientation, self.surf)
            case _:
                print("HEH")

class Lazer(pygame.sprite.Sprite):
    def __init__(self, game, image, rect, pos, length, thickness, orientation, surf):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = image
        
        self.pos = pos
        
        self.surf = surf
        
        self.TotalLength = length
        
        self.thickness = thickness
        
        self.totalTimeTaken = 0.1
        self.currentTimeTaken = 0.0
        
        self.currentLength = 0.0
        
        self.orientation = orientation
        
        self.LIFETIME = 0.3
        self.currentTime = 0.0
        
        match self.orientation:
            case 'Horizontal-L':
                self.rect = pygame.Rect(self.pos[0], self.pos[1], self.currentLength, self.thickness)
                pygame.draw.rect(self.surf, (255, 0, 0, 255), self.rect)
            case 'Vertical-L':
                self.rect = pygame.Rect(self.pos[0], self.pos[1], self.thickness, self.currentLength)
                pygame.draw.rect(self.surf, (255, 0, 0, 255), self.rect)
                
        self.game.LazerGroup.add(self)
        
    def update(self, dt=1):
        if self.currentTimeTaken < self.totalTimeTaken:   self.currentTimeTaken += dt
        else:                                   self.currentTimeTaken = self.totalTimeTaken
        
        self.currentLength = (self.currentTimeTaken / self.totalTimeTaken) * self.TotalLength
        
        match self.orientation:
            case 'Horizontal-L':
                self.rect = pygame.Rect(self.pos[0], self.pos[1], self.currentLength, self.thickness)
                pygame.draw.rect(self.surf, (255, 0, 0, 255), self.rect)
            case 'Vertical-L':
                self.rect = pygame.Rect(self.pos[0], self.pos[1], self.thickness, self.currentLength)
                pygame.draw.rect(self.surf, (255, 0, 0, 255), self.rect)
        
        if self.rect.colliderect(self.game.player.rect):
            self.game.SetGameOver()
                
        if self.currentTime < self.LIFETIME:    self.currentTime += dt
        else:                                   self.kill()