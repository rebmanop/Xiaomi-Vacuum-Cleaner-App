from enum import Enum

class Fanspeed(Enum):
    Silent = 101
    Standart = 102
    Medium = 103
    Turbo = 104
    Gentle = 105
    Auto = 106  


class Status: 
    
    def __init__(self, bot) -> None:
        self.update(bot)

        
    def update(self, bot):
        self.status_obj = bot.status()
        self.parse_status() 
        self.create_list()
       

    def parse_status(self):
        if self.status_obj.fanspeed == Fanspeed.Silent.value:
            self.fanspeed = "Silent"
            
        elif self.status_obj.fanspeed == Fanspeed.Standart.value:
            self.fanspeed = "Standart"
        
        elif self.status_obj.fanspeed == Fanspeed.Medium.value:
            self.fanspeed = "Medium"
        
        elif self.status_obj.fanspeed == Fanspeed.Turbo.value:
            self.fanspeed = "Turbo"
        
        elif self.status_obj.fanspeed == Fanspeed.Gentle.value:
            self.fanspeed = "Gentle"
        
        elif self.status_obj.fanspeed == Fanspeed.Auto.value:
            self.fanspeed = "Auto"
        
        
        if self.status_obj.got_error == False:
            self.got_error = "No errors"

        else:
            self.got_error = f"Error code: {self.status_obj.error_code}"


        if self.status_obj.is_paused == True:
            self.is_paused = "Is paused"

        else: 
            self.is_paused = "Is not paused"
            

        self.state = f"{self.status_obj.state}"
        self.battery_level = f"{self.status_obj.battery}%"
        self.error_code = f"Error code: {self.status_obj.error_code}"
        

    def create_list(self):
        self.status_list = []
        
        self.status_list.append(self.state)
        self.status_list.append(self.battery_level)
        self.status_list.append(self.got_error)
        self.status_list.append(self.is_paused)
        self.status_list.append(self.fanspeed)

    def get_status_list(self) -> list[str]:
        return self.status_list

    def get_status_obj(self):
        return self.status_obj

    def get_status_str(self) -> str:
        return self.status_str


   
     





    
    
    

        

         







    
    
