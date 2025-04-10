import board
import busio
import adafruit_gps
import time

class gps:
    def __init__(self, tx=board.GP4, rx=board.GP5, baudrate=9600, timeout=10):
        """Initialize GPS using UART."""
        self.uart = busio.UART(tx, rx, baudrate=baudrate, timeout=timeout)
        self.gps = adafruit_gps.GPS(self.uart, debug=False)

        # Configure GPS update rate (1 Hz)
        self.gps.send_command(b"PMTK220,1000")  # Update every second
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")  # Enable GGA & RMC sentences

    def update(self):
        """Update GPS data. Returns a dictionary with GPS info or None if no fix."""
        self.gps.update()

        if not self.gps.has_fix:
            return None  # No GPS fix yet

        return {
            "latitude": self.gps.latitude,
            "longitude": self.gps.longitude,
            "altitude": self.gps.altitude_m,
            "speed_knots": self.gps.speed_knots,
            "satellites": self.gps.satellites
        }
