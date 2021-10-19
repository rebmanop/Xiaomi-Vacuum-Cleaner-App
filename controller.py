import pygame
from miio.vacuum import Vacuum


class Controller:
    
    def __init__(self, bot: Vacuum):
        self.bot = bot
        self.rot = 0
        self.rot_delta = 30 
        self.rot_min = Vacuum.MANUAL_ROTATION_MIN
        self.rot_max = Vacuum.MANUAL_ROTATION_MAX
        self.vel = 0.0
        self.vel_delta = 0.1
        self.vel_min = Vacuum.MANUAL_VELOCITY_MIN
        self.vel_max = Vacuum.MANUAL_VELOCITY_MAX
        self.dur = 500 #0.15 of a second 
        pygame.joystick.init()
        if pygame.joystick.get_count() != 0:
            self.joystick_is_connected = True
            self.joystick = pygame.joystick.Joystick(0)
        else:
            self.joystick_is_connected = False


    def handle_movement(self) -> None:
        keys_pressed = pygame.key.get_pressed()
       
        self.dispatch_control(keys_pressed)
        return self.info()


    def scale_joystick_values(self, value, stick1_min, stick1_max, stick2_min, stick2_max) -> float:
        stick1_span = stick1_max - stick1_min
        stick2_span = stick2_max - stick2_min
        scaled_value = float(value - stick1_min) / float(stick1_span)
        return stick2_min + (scaled_value * stick2_span)


    def dispatch_control(self, keys_pressed) -> None:
        self.vel = 0
        self.rot = 0
        
        if self.joystick_is_connected == True:
            if self.joystick.get_axis(2) != 0:
                self.rot = -self.scale_joystick_values(self.joystick.get_axis(2), -1, 1, -90, 90)
                if abs(self.rot) < 8:
                    self.rot = 0

            if self.joystick.get_axis(1) != 0:
                self.vel = -self.scale_joystick_values(self.joystick.get_axis(1), -1, 1, self.vel_min, self.vel_max)
                if abs(self.vel) < 0.07:
                    self.vel = 0

            if self.rot or self.vel:
                self.bot.manual_control(self.rot, self.vel, self.dur)

        else:   
            if keys_pressed[pygame.K_w]:
                self.vel = min(self.vel + self.vel_delta, self.vel_max)
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)

            elif keys_pressed[pygame.K_s]:
                self.vel = max(self.vel - self.vel_delta, self.vel_min)
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)


            if keys_pressed[pygame.K_w] and keys_pressed[pygame.K_LSHIFT]:
                self.vel = 0 if self.vel < 0 else self.vel_max
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)

            elif  keys_pressed[pygame.K_s] and keys_pressed[pygame.K_LSHIFT]:
                self.vel = 0 if self.vel > 0 else self.vel_min
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)


            if keys_pressed[pygame.K_a]:
                self.rot = min(self.rot + self.rot_delta, self.rot_max)
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)
            
            elif keys_pressed[pygame.K_d]:
                self.rot = max(self.rot - self.rot_delta, self.rot_min)
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)


            if keys_pressed[pygame.K_a] and keys_pressed[pygame.K_LSHIFT]:
                self.rot = 0 if self.rot < 0 else self.rot_max
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)

            elif keys_pressed[pygame.K_d] and keys_pressed[pygame.K_LSHIFT]:
                self.rot = 0 if self.rot > 0 else self.rot_min
                self.bot.manual_control(rotation=self.rot, velocity=self.vel, duration=self.dur)

        
    def info(self) -> tuple:
        return self.rot, self.vel
