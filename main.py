import machine
import time
import ubinascii
import webrepl
import dht

from umqtt.simple import MQTTClient

# These defaults are overwritten with the contents of /config.json by load_config()
CONFIG = {
    "broker": "iot.eclipse.org",
	"port" : 1883,
    "sensor_pin": 4, 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"sjm/temperature",
}

client = None

def load_config():
    import ujson as json
    try:
        with open("/config.json") as f:
            config = json.loads(f.read())
    except (OSError, ValueError):
        print("Couldn't load /config.json")
        save_config()
    else:
        CONFIG.update(config)
        print("Loaded config from /config.json")

def save_config():
    import ujson as json
    try:
        with open("/config.json", "w") as f:
            f.write(json.dumps(CONFIG))
    except OSError:
        print("Couldn't save /config.json")

def main():
	sensor_pin = CONFIG['sensor_pin']
	client = MQTTClient(CONFIG['client_id'], CONFIG['broker'], CONFIG['port'])
	client.connect()
	print("Connected to {}".format(CONFIG['broker']))
	while True:
		data = dht.DHT11(machine.Pin(sensor_pin))
		data.measure()
		client.publish(CONFIG['topic'], bytes(str(data.temperature()), 'utf-8'))
		print('Sensor state: {}'.format(data.temperature()))
		time.sleep(5)

if __name__ == '__main__':
	load_config()
	main()
