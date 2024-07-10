import pygame

class Text:
    def __init__(self, game, text, text_size, pos, font='Ariel' ,text_col=(255,255,255)):
        self.game = game
        self.font = font
        self.text_size = text_size
        self.fontImage = pygame.font.SysFont(self.font, self.text_size)
        self.pos = pos
        self.text_col = text_col
        self.text_size = text_size
        self.text = text
        self.img = self.fontImage.render(self.text, True, self.text_col)
        self.text_width = self.img.get_width
        self.text_height = self.img.get_height
    
    def draw(self, surf):
        surf.blit(self.img, self.pos)
    
    def dynamicDraw(self, surf, text):
        self.img = self.fontImage.render(text, True, self.text_col)
        surf.blit(self.img, self.pos)
        
    def ChangePosition(self, pos):
        self.pos = pos
    
    def ChangeFontSize(self, size):
        self.text_size = size
        self.fontImage = pygame.font.SysFont(self.font, self.text_size)

    def display_text(self, surface):
        collection = [word.split(' ') for word in self.text.splitlines()]
        space = self.fontImage.size(' ')[0]
        x,y = self.pos
        for lines in collection:
            for words in lines:
                word_surface = self.fontImage.render(words, True, self.text_col)
                word_width , word_height = word_surface.get_size()
                if x + word_width >= 800:
                    x = self.pos[0]
                    y += word_height
                surface.blit(word_surface, (x,y))
                x += word_width + space
            x = self.pos[0]
            y += word_height