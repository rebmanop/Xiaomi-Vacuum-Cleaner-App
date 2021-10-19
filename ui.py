import pygame
import os
import urllib.request as urllib
import numpy as np
from pygame.constants import BUTTON_LEFT
import requests, io
from PIL import Image, ImageFile
from status import Status
from utils import scale_image, blit_text


Image.LOAD_TRUNCATED_IMAGES = True
ImageFile.LOAD_TRUNCATED_IMAGES = True
pygame.font.init()


WIDTH, HEIGHT = 720, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Xiaomi Vacuum Cleaner App")
URL='http://192.168.1.31:8080/shot.jpg'
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255,73,0)
CREATED_BY_FONT = pygame.font.SysFont('arial', 15)
MANUAL_INFO_FONT = pygame.font.SysFont('arial', 20)
BUTTON_FONT = pygame.font.SysFont('arial', 22)
STATUS_FONT = pygame.font.SysFont('arial', 22)
TITLE_FONT = pygame.font.SysFont('arial', 50)
TITLE_IMG = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'banner_main_menu.png')).convert_alpha(), (609, 103))
XIAOMI_LOGO = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'xiaomi_3.png')).convert_alpha(), (35, 35))
UP_ARROW = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'up_arrow.png')).convert_alpha(), (51, 51))
DOWN_ARROW = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'down_arrow.png')).convert_alpha(), (51, 51))
LEFT_ARROW = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'left_arrow.png')).convert_alpha(), (51, 51))
RIGHT_ARROW = pygame.transform.scale(pygame.image.load(os.path.join('imgs', 'right_arrow.png')).convert_alpha(), (51, 51))
BATTERY_IMG = pygame.image.load(os.path.join('imgs', 'battery_level.png')).convert_alpha()
FAN_IMG = scale_image(pygame.image.load(os.path.join('imgs', 'ac.png')).convert_alpha(), 0.05)
UPDATE_IMG = scale_image(pygame.image.load(os.path.join('imgs', 'refresh.png')).convert_alpha(), 0.05)
STATE_IMG = scale_image(pygame.image.load(os.path.join('imgs', 'state.png')).convert_alpha(), 0.05)
ERROR_IMG = scale_image(pygame.image.load(os.path.join('imgs', 'error.png')).convert_alpha(), 0.05)
PAUSE_IMG = scale_image(pygame.image.load(os.path.join('imgs', 'pause.png')).convert_alpha(), 0.05)
BATTERY_IMG_STATUS = scale_image(pygame.image.load(os.path.join('imgs', 'battery_level.png')).convert_alpha(), 0.5)


def get_image() -> np.array:
    response = requests.get(URL)
    bytes_img = io.BytesIO(response.content)
    array_img = np.array(Image.open(bytes_img))
    return array_img


def transform_image() -> pygame.Surface:
    array_img = get_image()

    surface = pygame.surfarray.make_surface(array_img)
    surface =  pygame.transform.flip(surface, False, True)
    surface =  pygame.transform.rotate(surface, -90)

    return surface

    
def blit_status(status_list, font, color, surface, x ,y) -> None:
    for each in status_list:
        status_img = font.render(each, True, color)
        surface.blit(status_img, (x, y))
        y += 30      #step in px's betwen each line


def draw_menu(WIN, manual_mode_button, go_home_button, check_status_button) -> None:
    WIN.fill(ORANGE)
    WIN.blit(TITLE_IMG, (WIN.get_width() / 2 - TITLE_IMG.get_width() / 2, 20))
    WIN.blit(XIAOMI_LOGO, (10, WIN.get_height() - XIAOMI_LOGO.get_height()))

    blit_text("Created by beenin", CREATED_BY_FONT, BLACK, WIN, False, False, WIN.get_width() - 105, WIN.get_height() - 20)
    manual_mode_button.blit(WIN, outline = BLACK)
    go_home_button.blit(WIN, outline = BLACK)
    check_status_button.blit(WIN, outline = BLACK)

    pygame.display.update()


def blit_direction(rot_info, vel_info):
    if vel_info > 0:
        WIN.blit(UP_ARROW, (UP_ARROW.get_width(), WIN.get_height() - UP_ARROW.get_height() * 2))
    elif vel_info < 0:
        WIN.blit(DOWN_ARROW, (DOWN_ARROW.get_width(), WIN.get_height() - DOWN_ARROW.get_height()))

    if rot_info > 0:
        WIN.blit(LEFT_ARROW, (0, WIN.get_height() - LEFT_ARROW.get_height()))
    elif rot_info < 0:
        WIN.blit(RIGHT_ARROW, (RIGHT_ARROW.get_width() * 2, WIN.get_height() - RIGHT_ARROW.get_height()))


def draw_manual(WIN, current_status, movement_info) -> None:
    video_feed = transform_image()  
    rot_info, vel_info = movement_info
    
    WIN.fill(BLACK)
    WIN.blit(video_feed, (0,0))
    blit_direction(rot_info, vel_info)
    blit_text(f"Rotation: {rot_info:.1f}    Velocity: {vel_info:.2f}", MANUAL_INFO_FONT, WHITE, WIN, False, False, WIN.get_width() / 1.5, WIN.get_height() - 30)
    WIN.blit(BATTERY_IMG, (WIDTH - BATTERY_IMG.get_width(), -10))
    blit_text(f"{(current_status.get_status_obj()).battery}%", CREATED_BY_FONT, WHITE, WIN, False, False, WIDTH - BATTERY_IMG.get_width()  / 2 - 15, -10 + BATTERY_IMG.get_height() / 2.7)

    pygame.display.update()


def draw_status_menu(WIN, current_status, status_update_button):
    WIN.fill(ORANGE)
    blit_status(current_status.get_status_list(), STATUS_FONT, BLACK, WIN, WIDTH /2 - 100 + STATE_IMG.get_width() + 10, 150) # 10 is offset
    status_update_button.blit(WIN, outline = BLACK)
    WIN.blit(STATE_IMG, (WIDTH /2 - 100, 150))
    WIN.blit(BATTERY_IMG_STATUS, (WIDTH /2 - 100, 180))
    WIN.blit(ERROR_IMG, (WIDTH /2 - 100, 210))
    WIN.blit(PAUSE_IMG, (WIDTH /2 - 100, 240))
    WIN.blit(FAN_IMG, (WIDTH /2 - 100, 270))


    WIN.blit(UPDATE_IMG, (WIDTH -  status_update_button.get_width() / 2 - UPDATE_IMG.get_width() / 2, HEIGHT -  status_update_button.get_height() / 2 - UPDATE_IMG.get_height() / 2))
  
    pygame.display.update()


def draw_go_home_menu(WIN, go_home_button):
    WIN.fill(ORANGE)

    go_home_button.blit(WIN, outline = BLACK)
    
    pygame.display.update()
