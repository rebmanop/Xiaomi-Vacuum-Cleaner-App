import pygame 
def scale_image(image, factor):
   scaled_image =  pygame.transform.scale(image, (int(image.get_width() * factor), int(image.get_height() * factor)))
   return scaled_image

