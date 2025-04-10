import board
import busio
import adafruit_bmp280

# define the I2C pins
i2c1 = busio.I2C(board.GP7, board.GP6)

# Create BMP280 object
bmp280_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c1, address=0x76)




# read temperature and pressure
def read_temperature():
    return bmp280_sensor.temperature


def read_pressure():
    return bmp280_sensor.pressure
