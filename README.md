# SmartGrow
 Marittya Keu
 IOT Project Name: SmartGrow
 Special Topics: IOT 

High Level Function Description:
My project was created and written in Python to help automate the agricultural industry by creating a smart watering system. With the help of a Raspberry Pi 3 and some other hardware, it is able to sense soil moisture level and dispense water. All functionality can be managed through a website being served by a local web server via the Raspberry Pi. The goal is simple, when in a good state, the green LED is turned on, otherwise the red LED is turned on when the soil is dry. MariaDB was used to store credentials to login to the website to manage the functionality. Once logged in, you can manually get soil moisture levels, dispense water, or automate the process. Automating the process, checks for the soil level, if in a good state, it displays a message. However, if the soil is dry, it dispenses water and also send an e-mail via smtp. In my opinion, technology is tapping into many industries to help automate manual labor and this project accomplishes that. SmartGrow allows you to receive alerts and monitor your garden remotely and can improve cost efficiency. 

# Hardware Used:
1. Raspberry Pi 3
2. Breadboard
3. MCP3008 analog to digital converter chip
4. Red and Green LEDs
5. 12v water control solenoid valve
6. 12v power supply
7. Single channel relay switch
8. Vegetronix Soil Moisture Sensor

# Software/Packages Used:
1. MariaDB – SQL database used to store login credentials
2. Python
3. Flask – Python web Microframework used to make connection to DB
4. SMTP – TCP/IP protocol for sending and receiving e-mail
5. Bootstrap CDN

