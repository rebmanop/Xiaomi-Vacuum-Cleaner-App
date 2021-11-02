import miio
import pygame
import ui
import sys
import time
import button
import status
import configparser
import threading
import multiprocessing
from itertools import cycle
from controller import Controller


config = configparser.ConfigParser()
config.read('config.txt')


IP = config['DEFAULT']['IP']
TOKEN = config['DEFAULT']['TOKEN']
FPS = 30
STATUS_UPDATE_TIMER = 30  #in seconds


bot = miio.vacuum.Vacuum(IP, TOKEN)
main_clock = pygame.time.Clock()
current_status = status.Status(bot)
manual_mode_button = button.Button(ui.WHITE, ui.WIDTH / 2 , 150, 250, 40, ui.BUTTON_FONT, ui.BLACK, 'manual mode', True)
go_home_button = button.Button(ui.WHITE, ui.WIDTH / 2, 240, 250, 40, ui.BUTTON_FONT, ui.BLACK, 'go home', True)
check_status_button = button.Button(ui.WHITE, ui.WIDTH / 2, 330, 250, 40, ui.BUTTON_FONT, ui.BLACK, 'settings', True)
status_update_button = button.Button(ui.WHITE, ui.WIDTH - 60, 10, 50, 50, ui.BUTTON_FONT, ui.BLACK)
find_bot_button = button.Button(ui.WHITE, ui.WIDTH - 60, 70, 50, 50, ui.BUTTON_FONT, ui.BLACK)
change_fanspeed_button = button.Button(ui.WHITE, ui.WIDTH/2 , ui.HEIGHT /2, 300, 50, ui.BUTTON_FONT, ui.BLACK, 'change fanspeed', True, True)
pool = cycle([fanspeed.value for fanspeed in status.Fanspeed]) #iterates in a loop through a list of enum values
controller = Controller(bot)


def main_menu():

    while True:
        mpos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if manual_mode_button.has_mouse_on_it(mpos):
                    manual_mode()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_status_button.has_mouse_on_it(mpos):
                    settings_menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if go_home_button.has_mouse_on_it(mpos):
                    go_home()


            if event.type == pygame.MOUSEMOTION:
                if manual_mode_button.has_mouse_on_it(mpos):
                    manual_mode_button.color = ui.GREEN
                else:
                    manual_mode_button.color = ui.WHITE

            if event.type == pygame.MOUSEMOTION:
                if go_home_button.has_mouse_on_it(mpos):
                    go_home_button.color = ui.GREEN
                else:
                    go_home_button.color = ui.WHITE

            if event.type == pygame.MOUSEMOTION:
                if check_status_button.has_mouse_on_it(mpos):
                    check_status_button.color = ui.GREEN
                else:
                    check_status_button.color = ui.WHITE
                

        ui.draw_main_menu(ui.WIN, manual_mode_button, go_home_button, check_status_button)
        main_clock.tick(FPS)


def manual_mode():
    bot.set_fan_speed(status.Fanspeed.Gentle.value)
    bot.manual_start()
    current_status.update(bot)
    status_timer = 0
    running = True 
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bot.manual_stop()
                bot.set_fan_speed(status.Fanspeed.Turbo.value)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    bot.manual_stop()
                    bot.set_fan_speed(status.Fanspeed.Turbo.value)

        if status_timer == STATUS_UPDATE_TIMER * FPS:
            current_status.update(bot)
            status_timer = 0

        movement_info = controller.handle_movement()
        ui.draw_manual(ui.WIN, current_status, movement_info)
        main_clock.tick(FPS)
        status_timer += 1


def settings_menu():
    current_status.update(bot)
    running = True 
    status_timer = 0
    while running:
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                if status_update_button.has_mouse_on_it(mpos):
                    current_status.update(bot)
                    status_timer = 0

            if event.type == pygame.MOUSEMOTION:
                if status_update_button.has_mouse_on_it(mpos):
                    status_update_button.color = ui.GREEN
                else:
                    status_update_button.color = ui.WHITE


            if event.type == pygame.MOUSEBUTTONDOWN:
                if find_bot_button.has_mouse_on_it(mpos):
                    bot.find()
                    
            if event.type == pygame.MOUSEMOTION:
                if find_bot_button.has_mouse_on_it(mpos):
                    find_bot_button.color = ui.GREEN
                else:
                    find_bot_button.color = ui.WHITE


            if event.type == pygame.MOUSEBUTTONDOWN:
                if change_fanspeed_button.has_mouse_on_it(mpos):
                    bot.set_fan_speed(next(pool))
                    current_status.update(bot)
                    
                    
            if event.type == pygame.MOUSEMOTION:
                if change_fanspeed_button.has_mouse_on_it(mpos):
                    change_fanspeed_button.color = ui.GREEN
                else:
                    change_fanspeed_button.color = ui.WHITE


        if status_timer == STATUS_UPDATE_TIMER * FPS:
            current_status.update(bot)
            status_timer = 0

        ui.draw_settings_menu(ui.WIN, current_status, status_update_button, find_bot_button, change_fanspeed_button, STATUS_UPDATE_TIMER)
        main_clock.tick(FPS)
        status_timer += 1

       

def go_home():
    bot.home()
    time.sleep(2) #waits until bot.home() is done
    go_home_button.color = ui.WHITE
    frame_number = 1
    current_status.update(bot)
    while current_status.status_obj.state == "Returning home":
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break
            
            
        current_status.update(bot)

        
        if (frame_number == FPS / 5):

            go_home_button.text = "returning home.  "

        elif (frame_number == FPS / 2):
            go_home_button.text = "returning home.. "
        
        elif (frame_number == FPS / 1.2): 
            go_home_button.text = "returning home..."
        

        ui.draw_go_home_menu(ui.WIN, go_home_button)
        
        if frame_number >= FPS:
            frame_number = 0

        main_clock.tick(FPS)
        frame_number += 1
    
    go_home_button.text = "go home"


def clean_mode():
    #TODO
    pass


if __name__ == '__main__':
    main_menu()