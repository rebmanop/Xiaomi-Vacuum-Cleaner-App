import miio
import pygame
import requests
import ui
import sys
import time
import button
import status
import requests
import configparser
from itertools import cycle
from controller import Controller


#GET CONFIG
config = configparser.ConfigParser()
config.read('config_test.txt')
IP = config['DEFAULT']['IP']
TOKEN = config['DEFAULT']['TOKEN']


FPS = 30
STATUS_UPDATE_TIMER = 30  #in seconds


#OBJECT INITIALIZATION
bot = miio.vacuum.Vacuum(IP, TOKEN)
main_clock = pygame.time.Clock()
current_status = status.Status(bot)
manual_mode_button = button.Button(ui.GRAY, ui.WIDTH / 2 , 170, 250, 40, ui.BUTTON_FONT, ui.BLACK, 'manual mode', True)
go_home_button = button.Button(ui.GRAY, ui.WIDTH / 2, 260, 250, 40, ui.BUTTON_FONT, ui.BLACK, 'go home', True)
check_status_button = button.Button(ui.GRAY, ui.WIDTH / 2, 350, 250, 40, ui.BUTTON_FONT, ui.BLACK, 'settings', True)
status_update_button = button.Button(ui.WHITE, ui.WIDTH - 60, 10, 50, 50, ui.BUTTON_FONT, ui.BLACK)
find_bot_button = button.Button(ui.WHITE, ui.WIDTH - 60, 70, 50, 50, ui.BUTTON_FONT, ui.BLACK)
change_fanspeed_button = button.Button(ui.WHITE, ui.WIDTH/2 , ui.HEIGHT /2, 300, 50, ui.BUTTON_FONT, ui.BLACK, 'change fanspeed', True, True)
pool = cycle([fanspeed.value for fanspeed in status.FanspeedV2]) #loops through a list of enum values
controller = Controller(bot)


def main_menu():
    
    if  current_status.connected:
        check_status_button.color = ui.WHITE
        manual_mode_button.color = ui.WHITE
        go_home_button.color = ui.WHITE

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

            if current_status.connected:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if manual_mode_button.has_mouse_on_it(mpos):
                        manual_mode()

            if current_status.connected:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if check_status_button.has_mouse_on_it(mpos):
                        settings_menu()

            if current_status.connected:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if go_home_button.has_mouse_on_it(mpos):
                        go_home()

            if current_status.connected:
                if event.type == pygame.MOUSEMOTION:
                    if manual_mode_button.has_mouse_on_it(mpos):
                        manual_mode_button.color = ui.GREEN
                    else:
                        manual_mode_button.color = ui.WHITE

            if current_status.connected:
                if event.type == pygame.MOUSEMOTION:
                    if go_home_button.has_mouse_on_it(mpos):
                        go_home_button.color = ui.GREEN
                    else:
                        go_home_button.color = ui.WHITE

            if current_status.connected:
                if event.type == pygame.MOUSEMOTION:
                    if check_status_button.has_mouse_on_it(mpos):
                        check_status_button.color = ui.GREEN
                    else:
                        check_status_button.color = ui.WHITE
                

        ui.draw_main_menu(ui.WIN, manual_mode_button, go_home_button, check_status_button, current_status)
        main_clock.tick(FPS)


def manual_mode():
    video_feed_connected = True
    try:
        requests.get(ui.URL)
    except requests.exceptions.ConnectionError as e:
        video_feed_connected = False
        print(e)

    if video_feed_connected:
        bot.set_fan_speed(status.FanspeedV2.Gentle.value)
        bot.manual_start()
        current_status.update(bot)
        status_timer = 0
        running = True 
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    bot.manual_stop()
                    bot.set_fan_speed(status.FanspeedV2.Turbo.value)
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        bot.manual_stop()
                        bot.set_fan_speed(status.FanspeedV2.Turbo.value)

            if status_timer == STATUS_UPDATE_TIMER * FPS:
                current_status.update(bot)
                status_timer = 0

            movement_info = controller.handle_movement()
            ui.draw_manual(ui.WIN, current_status, video_feed_connected, manual_mode_button, movement_info)
            main_clock.tick(FPS)
            status_timer += 1
    else:
        frame_number = 1
        manual_mode_button.color = ui.WHITE
        manual_mode_button.text = "can't get video"
        while frame_number <= FPS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
            
            ui.draw_manual(ui.WIN, current_status,  video_feed_connected, manual_mode_button)
            main_clock.tick(FPS)
            frame_number += 1  
        manual_mode_button.text = "manual mode"


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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if find_bot_button.has_mouse_on_it(mpos):
                    bot.find()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if change_fanspeed_button.has_mouse_on_it(mpos):
                    bot.set_fan_speed(next(pool))
                    current_status.update(bot)

                    
            if event.type == pygame.MOUSEMOTION:
                if find_bot_button.has_mouse_on_it(mpos):
                    find_bot_button.color = ui.GREEN
                else:
                    find_bot_button.color = ui.WHITE


            if event.type == pygame.MOUSEMOTION:
                if change_fanspeed_button.has_mouse_on_it(mpos):
                    change_fanspeed_button.color = ui.GREEN
                else:
                    change_fanspeed_button.color = ui.WHITE
                    
            if event.type == pygame.MOUSEMOTION:
                if status_update_button.has_mouse_on_it(mpos):
                    status_update_button.color = ui.GREEN
                else:
                    status_update_button.color = ui.WHITE


        if status_timer == STATUS_UPDATE_TIMER * FPS:
            current_status.update(bot)
            status_timer = 0

        ui.draw_settings_menu(ui.WIN, current_status, status_update_button, find_bot_button, change_fanspeed_button, STATUS_UPDATE_TIMER)
        main_clock.tick(FPS)
        status_timer += 1

       
def go_home():
    current_status.update(bot)
    if current_status.status_obj.state == "Charging":
        frame_number = 1
        go_home_button.color = ui.WHITE
        go_home_button.text = "already home"
        while frame_number <= FPS:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() 
                
            ui.draw_go_home_menu(ui.WIN, go_home_button)
            main_clock.tick(FPS)
            frame_number += 1    
    else:
        bot.home()
        time.sleep(2) #waits until bot.home() is done
        go_home_button.color = ui.WHITE
        frame_number = 1
        current_status.update(bot)
        while current_status.status_obj.state == "Returning home":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

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


if __name__ == '__main__':
    main_menu()
