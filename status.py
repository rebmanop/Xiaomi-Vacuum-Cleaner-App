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
        self.assemble_status_str()
       

    def parse_status(self):
        if self.status_obj.fanspeed == Fanspeed.Silent.value:
            self.fanspeed = "Fanspeed: Silent"
            
        elif self.status_obj.fanspeed == Fanspeed.Standart.value:
            self.fanspeed = "Fanspeed: Standart"
        
        elif self.status_obj.fanspeed == Fanspeed.Medium.value:
            self.fanspeed = "Fanspeed: Medium"
        
        elif self.status_obj.fanspeed == Fanspeed.Turbo.value:
            self.fanspeed = "Fanspeed: Turbo"
        
        elif self.status_obj.fanspeed == Fanspeed.Gentle.value:
            self.fanspeed = "Fanspeed: Gentle"
        
        elif self.status_obj.fanspeed == Fanspeed.Auto.value:
            self.fanspeed = "Fanspeed: Auto"
        
        
            
        self.state = f"State: {self.status_obj.state}"
        self.battery_level = f"Battery level: {self.status_obj.battery}%"
        self.error_code = f"Error code: {self.status_obj.error_code}"
        self.got_error = f"Any errors: {self.status_obj.got_error}"
        self.is_on = f"Is on: {self.status_obj.is_on}"
        self.is_paused = f"Is paused: {self.status_obj.is_paused}"


    def create_list(self):
        self.status_list = []
        if self.status_obj.error_code == 0:
            self.status_list.append(self.state)
            self.status_list.append(self.battery_level)
            self.status_list.append(self.got_error)
            #self.status_list.append(self.is_on)
            self.status_list.append(self.is_paused)
            self.status_list.append(self.fanspeed)
        else:
            self.status_list.append(self.state)
            self.status_list.append(self.battery_level)
            self.status_list.append(self.error_code)
            self.status_list.append(self.got_error)
            #self.status_list.append(self.is_on)
            self.status_list.append(self.is_paused)
            self.status_list.append(self.fanspeed)


    def assemble_status_str(self):
        if self.status_obj.error_code == 0:
            self.status_str = self.state + "\n" + self.battery_level + "\n" + self.fanspeed + "\n" + self.got_error + "\n" + self.is_on + "\n" + self.is_paused
        else:
            self.status_str = self.state + "\n" + self.battery_level + "\n" + self.fanspeed + "\n" + self.got_error + "\n" + self.error_code + "\n" + self.is_on + "\n" + self.is_paused


    def get_status_list(self) -> list[str]:
        return self.status_list

    def get_status_obj(self):
        return self.status_obj

    def get_status_str(self) -> str:
        return self.status_str


   
     





    
    
    

        

         







    
    
