import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, speed, dashDistance):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.speed = speed
        self.flip = False
        self.image = self.game.assets['player']
        self.rect = self.image.get_rect()
        self.rect.topleft = tuple(self.pos)

        self.canDash = True
        self.DashFrames = dashDistance
        self.currentDashInterval = self.DashFrames
        self.dashSpeed = self.speed * 5
        self.DashCoolDown = 1.5
        self.currentCoolDownTime = 0.0
        
        self.movableDistanceOutsideScreen = 20
        
    def update(self, movement=(0, 0), dt=1):
        if not self.game.isDashing:
            frame_movement = ((movement[0] * self.speed * dt) + self.velocity[0], (movement[1] * self.speed * dt) + self.velocity[1])
            if movement[0] > 0: self.flip = False
            elif movement[0] < 0: self.flip = True
            self.pos[0] += frame_movement[0]
            self.pos[1] += frame_movement[1]
        if self.pos[0] < -self.movableDistanceOutsideScreen:  self.pos[0] = self.game.ScreenSize[0] + self.movableDistanceOutsideScreen
        if self.pos[0] > self.game.ScreenSize[0] + self.movableDistanceOutsideScreen:  self.pos[0] = -self.movableDistanceOutsideScreen
        if self.pos[1] < -self.movableDistanceOutsideScreen: self.pos[1] = self.game.ScreenSize[1] + self.movableDistanceOutsideScreen
        if self.pos[1] > self.game.ScreenSize[1] + self.movableDistanceOutsideScreen: self.pos[1] = - self.movableDistanceOutsideScreen
        
        self.rect.topleft = tuple(self.pos)
        
    def dash(self, isDashing, movement=(0, 0), dt=1):
        if self.currentDashInterval > 0:
            if self.canDash and isDashing:
                PlayerDashRemenant(self.game, self.pos)
                frame_movement = ((movement[0] * self.dashSpeed * dt) + self.velocity[0], (movement[1] * self.dashSpeed * dt) + self.velocity[1])
                if movement[0] > 0: self.flip = False
                elif movement[0] < 0: self.flip = True
                self.pos[0] += frame_movement[0]
                self.pos[1] += frame_movement[1]
                self.currentDashInterval -= dt
        else:
            self.canDash = False
            self.currentDashInterval = self.DashFrames
            self.currentCoolDownTime = self.DashCoolDown
        if not self.canDash:
            self.game.isDashing = False
            if self.currentCoolDownTime <= 0:
                self.canDash = True
                self.currentCoolDownTime = 0
            else:
                self.currentCoolDownTime -= dt
        
    def render(self, surf):
        surf.blit(pygame.transform.flip(self.game.assets['player'], self.flip, False), self.pos)

class StaminaFood(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = list(pos)
        self.image = self.game.assets['food']
        self.rect = self.image.get_rect().scale_by(1.2)
        self.rect.center = pos
        
        self.game.foodsGroup.add(self)
        
        self.Lifetime = 1.5
        self.currentTime = 0.0
    
    def update(self):
        if self.rect.colliderect(self.game.player.rect):
            self.game.SCORE += 1
            self.kill()

class PlayerDashRemenant(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = list(pos)
        self.image = self.game.assets['player-dashremenants']
        self.image.set_alpha(25)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
        self.LIFETIME = 0.5
        self.currentTime = 0.0
        
        self.game.PlayerDashRemenantGroup.add(self)
    
    def update(self, dt=1):
        if self.currentTime < self.LIFETIME:    self.currentTime += dt
        else:                                   self.kill()