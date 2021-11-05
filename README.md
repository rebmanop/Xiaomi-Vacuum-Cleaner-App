# Description
This application should not be taken too seriously, it was built around one stupid idea, which is to ride around your apartment from anywhere in the world on a robot vacuum cleaner, but it has some basic "robot vacuum app" features as well. Robot vacuum cleaners usually don't have a forward pointing camera on board, so I had to use an external one (Android phone's camera). 
# How it works
Python **requests** image from web server, which runs on a phone. This is done using **IP webcam** Android app. Then **pygame** displays this image on the screen. To control robot movement and to get robot related information **python-miio** module is beeing used. 
# Dependencies
 - **pygame**
 - **miio** 
 - **configparser**
 - **pillow**
 - **numpy**
 - **requests**
# How to use
 1) Download or clone this repository.
 2) Extract to some location.
 3) Download IP webcam app on a phone and configure it:
      Resolution: 720x480, 
      Quality: 30 - optimal value
 4) Start server.
 5) Fill in the robot's network infomation and video feed url in the **config.txt** file.
 6) Run main.py from **Xiaomi-Vacuum-Cleaner-App** folder.