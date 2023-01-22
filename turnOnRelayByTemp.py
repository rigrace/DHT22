import time
import adafruit_dht
import board

import gpiozero
from time import sleep
from gpiozero import LED
from pprint import pprint

relayPin = 18
sensorFailCntMax = 3
relay = LED("GPIO{}".format(relayPin), active_high=True, initial_value=None)
dht_device = adafruit_dht.DHT22(board.D4, use_pulseio=False)
sensorFailCnt = 0
sensorFailedLastTime = False
#On is below Off
relayOnTempCStr = input("Relay On Temp in C: ")
relayOnTempC = float(relayOnTempCStr)
relayOffTempCStr = input("Relay Off Temp in C: ")
relayOffTempC = float(relayOffTempCStr)

while True:
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9/5) + 32
        humid = dht_device.humidity
        print("Temp: {:.1f} F / {:.1f} C; Humidity: {}%".format(temp_f, temp_c, humid))
        
        #if relay.value == 0 and temp_c < relayOffTempC:
        #    Print Nothing to do, relay isw already in correct state"
        
        #Decide when to turn on relay and when to turn it off
        if temp_c <= relayOnTempC:
            relay.on()
        elif temp_c >= relayOffTempC:
            relay.off()
        
        #sensorFailedLastTime = False
        sensorFailCnt = 0
        
    except RuntimeError as error:
        sensorFailCnt += 1
        #sensorFailedLastTime = True
        print(error.args[0])
    #    time.sleep(2.0)
    #    
    #    continue
    except Exception as error:
        sensorFailCnt += 1
        #sensorFailedLastTime = True
    #    dht_device.exit()
    #    raise error
        print(error.args[0])
    finally:
        
        if sensorFailCnt >= sensorFailCntMax:
            print("Max sensor failed count. Turing off output relay.")
            relay.off()
            
        time.sleep(2.0)
