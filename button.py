import pygame

class Button:

    def __init__(self, color, x, y, width, height, font, font_color, text = '', centered_x = False, centered_y = False) -> None:

        if centered_x == True:
            self.x = x -  width / 2
        else:
            self.x = x

        if centered_y == True:
            self.y = y -  height / 2
        else:
            self.y = y

        self.color = color
        self.width = width
        self.height = height 
        self.text = text
        self.font = font
        self.font_color = font_color

       
    def blit(self, surface, outline = None):
        if outline:
            pygame.draw.rect(surface, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '': 
            text = self.font.render(self.text, 1, self.font_color)
            surface.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def has_mouse_on_it(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


    def get_width(self):
        return self.width


    def get_height(self):
        return self.height
 