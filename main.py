import machine
import time
import ubinascii
import webrepl
import dht

from umqtt.simple import MQTTClient

# These defaults are overwritten with the contents of /config.json by load_config()
"""CONFIG = {
    "broker": "iot.eclipse.org",
	"port" : 1883,
    "sensor_pin": 4, 
    "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
    "topic": b"sjm/temperature",
}"""

CONFIG = {
    "broker": "z1mppn.messaging.internetofthings.ibmcloud.com",
	"port" : 1883,
    "sensor_pin": 4, 
    "client_id": "d:z1mppn:teste:sjm",
	"username" : "use-token-auth",
	"password" : "V(LB-@6w&MpEEqFO3U",
    "topic": "iot-2/evt/temperature/fmt/json",
}

RETURNS = {
	'sensor': 'DHT11',
	'temperature': None,
	'humidity' : None
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
	import ujson as json
	sensor_pin = CONFIG['sensor_pin']
	#self, client_id, server, port=0, user=None, password=None, keepalive=0,ssl=False, ssl_params={})
	client = MQTTClient(CONFIG['client_id'], CONFIG['broker'], CONFIG['port'], CONFIG['username'], CONFIG['password'])
	client.connect()
	print("Connected to {}".format(CONFIG['broker']))
	while True:
		data = dht.DHT11(machine.Pin(sensor_pin))
		data.measure()
		RETURNS['temperature'] = data.temperature()
		RETURNS['humidity'] = data.humidity()
		client.publish(CONFIG['topic'], json.dumps(RETURNS))
		print('Sensor state: {}'.format(data.temperature()))
		time.sleep(5)

if __name__ == '__main__':
	load_config()
	main()
