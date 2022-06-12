# Description
This application should not be taken too seriously. It was built around one stupid idea, which is - riding around your apartment from anywhere in the world on a robot vacuum cleaner, it has some basic "robot vacuum app" functionality as well. Robot vacuum cleaners usually don't have a forward pointing camera on board, so I had to get creative... 
###### 
![This is an image](/imgs/Screenshots/photo.png)
# How it works
Python **requests** camera image from running on the phone web server. This is done using **IP webcam** android app. Then **pygame** displays received from server image on the screen. To control robot's movements and to get robot related information **python-miio** module is beeing used.
# Screenshots
###### main menu
![This is an image](/imgs/Screenshots/main.png)
###### remote control mode
![This is an image](/imgs/Screenshots/manual_mode.png)
###### settings and other stuff
![This is an image](/imgs/Screenshots/settings.png)
# Dependencies
 - **pygame**
 - **miio** 
 - **configparser**
 - **pillow**
 - **numpy**
 - **requests**
# How to use
I only had a chance to test it with 1S vacuum model, but it should work with similar models as well.
 1) Download or clone this repository.
 2) Extract to some location.
 3) Download IP webcam app on your android phone and configure it:
      Resolution: 720x480, 
      Quality: 30 - optimal value.
 5) Attach the phone to your vacuum cleaner and point it's camera forward.
 4) Start server.
 5) Fill in the robot's network infomation and video feed url in the **config.txt** file.
 6) Run main.py from **Xiaomi-Vacuum-Cleaner-App** folder.
 
 # Demo
![This is a gif](/imgs/Screenshots/demo.gif)
