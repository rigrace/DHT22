import time
import adafruit_dht
import board
dht_device = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        temp_c = dht_device.temperature
        temp_f = temp_c * (9/5) + 32
        humid = dht_device.humidity
        print("Temp: {:.1f} F / {:.1f} C; Humidity: {}%".format(temp_f, temp_c, humid))
        
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    
    time.sleep(2.0)