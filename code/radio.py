import board
import busio
import digitalio
import adafruit_rfm9x

class CanSatRadio:
    def __init__(self, spi, cs_pin, rstdummy, frequency=433.0):
        """ Initialize LoRa radio module without reset """
        self.cs = digitalio.DigitalInOut(cs_pin)
        self.cs.direction = digitalio.Direction.OUTPUT

        self.rst = digitalio.DigitalInOut(rstdummy)  # Dummy pin
        self.rst.direction = digitalio.Direction.OUTPUT

        # SPI Bus
        self.rfm9x = adafruit_rfm9x.RFM9x(spi, self.cs, self.rst, frequency)
        self.rfm9x.tx_power = 20  # Set transmission power (max: 23 dBm)



    def send(self, message):
        """ Send a message via LoRa """
        self.rfm9x.send(message.encode())
        print(f"Sent: {message}")

    def receive(self):
        """ Receive a message """
        packet = self.rfm9x.receive(timeout=5.0)  # 5-second timeout
        if packet:
            message = str(packet, "utf-8")
            print(f"Received: {message}")
            return message
        return None

    def get_rssi(self):
        """ Get RSSI (signal strength) """
        return self.rfm9x.last_rssi




#message = radio.receive()
#if message:
#    print(f"Received: {message}")
#print(f"RSSI: {radio.get_rssi()} dBm")
