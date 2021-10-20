import pygame 


def scale_image(image, factor):
   scaled_image =  pygame.transform.scale(image, (int(image.get_width() * factor), int(image.get_height() * factor)))
   return scaled_image

def blit_text(text, font, color, surface, centered_x, centered_y, x = None, y = None):
    textobj = font.render(text, 1, color)

    if centered_x == True and centered_y == True:
        textrect = textobj.get_rect()
        textrect.topleft = (surface.get_width() / 2 - textrect.w / 2, surface.get_height() / 2 - textrect.h / 2)
        surface.blit(textobj, textrect)

    elif centered_x == True and centered_y == False:
        textrect = textobj.get_rect()
        textrect.topleft = (surface.get_width() / 2 - textrect.w /2, y)
        surface.blit(textobj, textrect)

    elif centered_x == False and centered_y == True:
        textrect = textobj.get_rect()
        textrect.topleft = (x, surface.get_height() / 2 - textrect.h / 2)
        surface.blit(textobj, textrect)

    else: 
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


def blit_status(status_list, font, color, surface, x , y, delta_y) -> None:
    for each in status_list:
        status_img = font.render(each, True, color)
        surface.blit(status_img, (x, y))
        y += delta_y     #step in px's betwen each line


