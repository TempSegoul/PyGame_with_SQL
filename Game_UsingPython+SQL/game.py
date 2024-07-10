import pygame
import pygame_gui
import sys

import random

from Scripts.entities import PhysicsEntity, StaminaFood
from Scripts.UIText import Text
from Scripts.utils import load_image
from Scripts.lightshow import LightShow
from Scripts.DATABASE import showAll, addplayer, CloseConnection

class Game:
    def __init__(self):
        pygame.init()

        self.isGameOver = False
        
        self.ActualScreenSize = (1280,720)
        self.ScreenSize = (640,360)
        
        pygame.display.set_caption("Game")
        self.screen = pygame.display.set_mode(self.ActualScreenSize)
        
        self.manager = pygame_gui.UIManager((1600, 900))

        self.text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 325), (600, 50)), manager=self.manager,
                                                    object_id='#main_text_entry', placeholder_text='Enter Username:')
        
        self.display = pygame.Surface(self.ScreenSize)
        self.UI = pygame.Surface(self.ActualScreenSize, pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        
        self.playerName = self.GetUsername()

        self.X_movement = [False, False]
        self.Y_movement = [False, False]
        self.isDashing = False
        
        self.assets = {
            'player' : load_image('Player/Idle/0.png'),
            'player-dashremenants' : load_image('Player/Idle/0.png'),
            'food' : load_image('StaminaFood/0.png')
        }
        
        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15), 180, 0.1)
        
        self.PlayerDashRemenantGroup = pygame.sprite.Group()
        
        self.foodsGroup = pygame.sprite.Group()        
        self.isFoodSpawned = False
        
        self.preLazerGroup = pygame.sprite.Group()
        self.LazerGroup = pygame.sprite.Group()
        
        self.LIGHTSHOW = LightShow(self, self.display)
        
        self.SCORE = 0
        
        self.ScoreTxt = Text(self, '0', 60, (self.ActualScreenSize[0] - 100, 40))
        
        self.GameOverText = Text(self, 'GAME OVER', 140, (self.ActualScreenSize[0] * 0.5, self.ActualScreenSize[1] * 0.5))
        
        self.EnterUsernameTxt = Text(self, 'ENTER USERNAME:', 100, (int(self.ActualScreenSize[0] * 0.25), int(self.ActualScreenSize[1] * 0.25)))
        self.usernameFieldTxT = Text(self, '', 90, (int(self.ActualScreenSize[0] * 0.5), int(self.ActualScreenSize[1] * 0.5)))
        
        self.dt = 0
        
        self.results = []
    
    def GetUsername(self) -> str:
        # self.EnterUsernameTxt.ChangePosition((self.ActualScreenSize[0] // 2 - self.EnterUsernameTxt.text_width // 2, (self.ActualScreenSize[1] // 2 - self.EnterUsernameTxt.text_height // 2) - 100))
        while True:
            self.screen.fill((100,150,100,255))
            self.dt = self.clock.tick(240) * 0.001
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                    return event.text
                
                self.manager.process_events(event)
            
            self.manager.update(self.dt)

            self.manager.draw_ui(self.screen)

            pygame.display.update()
            
        
    def run(self):        
        while True:
            if not self.isGameOver:
                self.display.fill((0,20,0))
                
                if len(self.foodsGroup.sprites()) == 0:
                    self.isFoodSpawned = False

                if not self.isFoodSpawned:
                    self.food = StaminaFood(self, (random.randint(100,self.display.get_width()-100), random.randint(100,self.display.get_height()-100)))
                    self.isFoodSpawned = True
                else:
                    self.foodsGroup.update()
                    self.foodsGroup.draw(self.display)
                
                self.PlayerDashRemenantGroup.update(self.dt)
                self.PlayerDashRemenantGroup.draw(self.display)
                
                self.player.update((self.X_movement[1] - self.X_movement[0], self.Y_movement[1] - self.Y_movement[0]), self.dt)
                self.player.dash(self.isDashing, (self.X_movement[1] - self.X_movement[0], self.Y_movement[1] - self.Y_movement[0]), self.dt)
                self.player.render(self.display)
                
                self.LIGHTSHOW.update(self.dt)
                
                # INPUTS ------------------------------------------------------------------------------>
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        CloseConnection()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:        # Key PRESSED
                        if event.key == pygame.K_w:     # W
                            self.Y_movement[0] = True
                        if event.key == pygame.K_s:     # S
                            self.Y_movement[1] = True
                        if event.key == pygame.K_a:     # A
                            self.X_movement[0] = True
                        if event.key == pygame.K_d:     # D
                            self.X_movement[1] = True
                        if event.key == pygame.K_SPACE: # Space (DASH)
                            self.isDashing = True
                    if event.type == pygame.KEYUP:          # Key NOT PRESSED ANYMORE
                        if event.key == pygame.K_w:     # W
                            self.Y_movement[0] = False
                        if event.key == pygame.K_s:     # S
                            self.Y_movement[1] = False
                        if event.key == pygame.K_a:     # A
                            self.X_movement[0] = False
                        if event.key == pygame.K_d:     # D
                            self.X_movement[1] = False

                # UI ELEMENTS ------------------------------------------------------------------------------>
                self.UI.fill((0,0,0,0))
                pygame.draw.rect(self.UI, (240, 255, 240, 40), pygame.Rect(30, 30, 230, 50))    # Background Fill for Dash Cooldown
                pygame.draw.rect(self.UI, (200, 255, 200, 255), pygame.Rect(30, 30, ((self.player.DashCoolDown - self.player.currentCoolDownTime) / self.player.DashCoolDown) * 230, 50))    # SLIDER Fill for Dash Cooldown
                
                self.ScoreTxt.dynamicDraw(self.UI, str(self.SCORE))
                
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                self.screen.blit(self.UI, (0, 0))
                
                pygame.display.update()
                self.dt = self.clock.tick(240) * 0.001
            else:
                self.UI.fill((0,0,0,255))
                self.GameOverText.draw(self.UI)
                self.ScoreTxt.ChangePosition((self.ActualScreenSize[0] * 0.5, (self.ActualScreenSize[1] * 0.5) + 100))
                self.ScoreTxt.ChangeFontSize(100)
                self.ScoreTxt.dynamicDraw(self.UI, "Score: " + str(self.SCORE))
                self.scoreboardTXT.display_text(self.UI)
                # INPUTS ------------------------------------------------------------------------------>
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        CloseConnection()
                        sys.exit()
                    # if event.type == pygame.KEYDOWN:  PLEASE DONT USE IT DOESNT WORK
                    #     self.RestartGame()
                
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
                self.screen.blit(self.UI, (0, 0))
                
                pygame.display.update()
                self.dt = self.clock.tick(240) * 0.001
    
    def SetGameOver(self):
        self.isGameOver = True
        self.Scoreboard()
            
    def RestartGame(self):  # PROBABLY BROKEN AF, JUST RESTART THE APPLICATION INSTEAD
        self.isGameOver = False
        self.SCORE = 0
    
    def Scoreboard(self):
        self.leadboard = ''''''
        addplayer(0, self.playerName, self.SCORE)
        self.results = showAll()
        self.leadboard += '''
        '''+'''%5s'''%'''Rank'''+'''%15s''' % '''Player name''' + '''%12s''' % '''Score'''
        for row in self.results[:10]:
            if self.results.index(row) == len(self.results):
                self.leadboard +=  str(self.results.index(row)+1) + '''%15s'''% str(row[1]) + '''%12s'''% str(row[2])
            else:
                self.leadboard += '''
                '''+ str(self.results.index(row)+1) + '''%15s'''% str(row[1]) + '''%12s'''% str(row[2])
                
        self.scoreboardTXT = Text(self, self.leadboard, 40, (50, 100), text_col=(200,200,150))
        
        
Game().run()