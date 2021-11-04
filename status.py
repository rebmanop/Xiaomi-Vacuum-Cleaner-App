from miio.vacuum import FanspeedV2

class Status: 
    
    def __init__(self, bot) -> None:
        self.status_obj = None
        self.got_error = "Unknown"
        self.fanspeed =  "Unknown"
        self.is_paused = "Unknown"
        self.status_list = []
        self.state = "Unknown"
        self.battery_level = "Unknown"
        self.error_code = "Unknown"
        self.info = bot.info()
        self.update(bot) 
        self.model = self.get_model()

    
    def get_model(self):
        model =  self.info.model
        return model
        

    def update(self, bot):
        self.status_obj = bot.status()
        self.parse_status() 
        self.create_list()
       

    def parse_status(self):
        if self.status_obj.fanspeed == FanspeedV2.Silent.value:
            self.fanspeed = "Silent"
            
        elif self.status_obj.fanspeed == FanspeedV2.Standard.value:
            self.fanspeed = "Standart"
        
        elif self.status_obj.fanspeed == FanspeedV2.Medium.value:
            self.fanspeed = "Medium"
        
        elif self.status_obj.fanspeed == FanspeedV2.Turbo.value:
            self.fanspeed = "Turbo"
        
        elif self.status_obj.fanspeed == FanspeedV2.Gentle.value:
            self.fanspeed = "Gentle"
        
        elif self.status_obj.fanspeed == FanspeedV2.Auto.value:
            self.fanspeed = "Auto"
        
        else: 
            self.fanspeed = "Unknown"
        
        
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




   
     





    
    
    

        

         







    
    
