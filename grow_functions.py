import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
import smtplib


########################################################
################### Variables ##########################
########################################################
RELAY_PIN = 21
RED_LED = 20
GREEN_LED = 16

def GPIOsetup(pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    
    
########################################################
### Activates solenoid valve to control water flow #####
########################################################
def activate_valve():
    GPIOsetup(RELAY_PIN)
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    print("Valve has been activated")
    time.sleep(2)
    GPIOsetup(RELAY_PIN)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    print("Valve has been DE-activated")
    soil_good()
    
    
   
############################################################
###### Get reading from soil moisture sensor via ###########
###### MCP3008 analog to digital converter #################
############################################################
# Software SPI configuration:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

def soil_moist_level():
    values = mcp.read_adc(0)
    return values



########################################################
################ LED controls ##########################
########################################################
def red_on():
    GPIOsetup(RED_LED)
    GPIO.output(RED_LED, 1)
    print("Soil moisture level is low.")
    
def red_off():
    GPIOsetup(RED_LED)
    GPIO.output(RED_LED, 0)

def green_on():
    GPIOsetup(GREEN_LED)
    GPIO.output(GREEN_LED, 1)
    time.sleep(1)
    
def green_off():
    GPIOsetup(GREEN_LED)
    GPIO.output(GREEN_LED, 0)

def soil_good():
    red_off()
    green_on()
    
def soil_bad():
    green_off()
    red_on()
    
def led_off():
    red_off()
    green_off()


########################################################
################# Send e-mail via smtp #################
########################################################
def send_email(from_addr, to_addr_list, cc_addr_list, subject,
               message, login, password,
               smtpserver='smtp.gmail.com:587'):
    header =  'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'CC: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n' % subject
    message = header + message
    
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems
 
 
#################################################################
#### Checks for soil moisture level if dry then #################
#### sends an email, turn red LED on, and dispense water ########
#### else in a good(watered soil) state, green LED is on ########
#################################################################
def auto_plant_email():
    while(True):
        if(soil_moist_level() < 200):
            soil_bad()
            send_email('marittyakeu@gmail.com',
                       ['ankimith1@hotmail.com', 'marittya_keu@yahoo.com'],
                       [''],
                       'Warning',
                       'The soil moisture level is low, and we just watered your plant!!!!!\n\nThe SmartGrow Team',
                       'marittyakeu@gmail.com',
                       'PaulPierce34')
            activate_valve()
        else:
            soil_good()


    
        

