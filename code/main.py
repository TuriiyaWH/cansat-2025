# external libraries
import digitalio
import time
import board
import storage
import busio


# internal libraries
import bmp280
from bmp280 import adafruit_bmp280
import radio
from radio import CanSatRadio
import gpsmodule
from gpsmodule import gps
import imu
from imu import BNO055_IMU
from sdcardmodule import SDStorage, is_sd_responsive
from adafruit_bitbangio import I2C

#alt in shed = 40m

# GPIO settings for LED
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

# check if the internal storage can be written to
write_en = not storage.getmount("/").readonly
print(f"Internal file writing enabled: {write_en}")

#initial packet count
packet_count = 0

# Initialize SPI with specified pins for SD card
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
cs_pin = board.GP17  # Chip Select
dummy_rst_pin = board.GP20

# Initialize radio
radio = CanSatRadio(spi, cs_pin, dummy_rst_pin)

#Initialize IMU
i2c0 = busio.I2C(board.GP9, board.GP8)
imu = BNO055_IMU(i2c0)

#bmp adjustment
adafruit_bmp280.overscan_temperature = 1
adafruit_bmp280.overscan_pressure = 1
adafruit_bmp280.mode = adafruit_bmp280.MODE_NORMAL
#temp = bmp280.read_temperature()
#pressure = bmp280.read_pressure()
#print(temp,pressure)

#initialize SD card and clear data
sd = SDStorage()
sd.clear_log("/sd/imudat.txt")
sd.clear_log("/sd/gpsdat.txt")
sd.clear_log("/sd/bmpdat.txt")

#Initialize gps
gps = gps()
gpsfix=False


#frequency control
time5hz = 0
led1hz = 0
bmp_last_read_time = 0  # Track last BMP280 read time
bmp_read_interval = 1  # Read every 1 second

#buffers
bmp_log_buffer = []
imu_log_buffer = []
gps_log_buffer = []

#time control
target_rate = 1/20
expected_time = 0  # Tracks the expected timestamp
start_time = time.monotonic()

while True:
    #20hz
    current_time = time.monotonic() - start_time

    led1hz += 1
    # toggle the LED
    if gpsfix is False:
        if time5hz >= 4 and gps_data:
            led.value = not led.value
    else:
        if led1hz >= 20:
            led.value = not led.value
            led1hz=0
            #print("LED.....")
    if current_time - bmp_last_read_time >= bmp_read_interval:
        try:
            temp = bmp280.read_temperature()
            pressure = bmp280.read_pressure()
            logg = f"T: {round(current_time,2)}, temp: {temp}, pressure: {pressure}"
            bmp_log_buffer.append(logg)
            #sd.write_log(logg,filename = "/sd/bmpdat.txt")
            radio.send(f"[HPS1] {logg}, pkt: {packet_count}")
            packet_count += 1
            #rint(temp,pressure)
            bmp_last_read_time = current_time
        except:
            print("error reading/writing bmp data")

    time5hz += 1
    if time5hz == 4:
        gps_data = gps.update()
        if gps_data:
            gpsfix=True
            log_entry = f"T: {round(current_time,2)}, lat: {gps_data['latitude']}, long: {gps_data['longitude']}, alt: {gps_data['altitude']}, spd: {gps_data['speed_knots']}, sat: {gps_data['satellites']}"
            #print(f"GPS Fix: {gps_data['latitude']}, {gps_data['longitude']}, {gps_data['altitude']}m")
            #print(f"Speed: {gps_data['speed_knots']} knots, Satellites: {gps_data['satellites']}")
            #sd.write_log(log_entry, filename="/sd/gpsdat.txt")
            gps_log_buffer.append(log_entry)
            radio.send(f"[HPS1] {log_entry}, pkt: {packet_count}")
            # increment the packet count
            packet_count += 1
        else:
            #print("Waiting for GPS fix...")
            #sd.write_log("NO FIX", filename="/sd/gpsdat.txt")
            gps_log_buffer.append(f"T: {round(current_time,2)}, NO FIX")
            #radio.send("[HPS1] NO GPS FIX")
        time5hz = 0


    try:
        orientation = imu.get_orientation()
        acceleration = imu.get_acceleration()
        magnetometer = imu.get_magnetometer()
        calibration = imu.is_calibrated()
    except:
       print("IMU ERROR")
    #print(f"Orient: {orientation}")
    #print(f"Accel : {acceleration}")
    #print(f"Magnet: {magnetometer}")
    #print(f"Calibration: {calibration}")

    log_entry = f"T: {current_time}, {orientation}, {acceleration}, {magnetometer}, {calibration}"
    imu_log_buffer.append(log_entry)
    #sd.write_log(log_entry, filename="/sd/imudat.txt")  # Write to SD card

    if len(imu_log_buffer) >= 10:
        sd.write_log("\n".join(imu_log_buffer), filename="/sd/imudat.txt")
        imu_log_buffer = [] # Clear buffer

    if len(gps_log_buffer) >= 10:
        sd.write_log("\n".join(gps_log_buffer), filename="/sd/gpsdat.txt")
        gps_log_buffer = [] # Clear buffer

    if len(bmp_log_buffer) >= 5:
        sd.write_log("\n".join(bmp_log_buffer), filename="/sd/bmpdat.txt")
        bmp_log_buffer = []  # Clear buffer

    loop_start = time.monotonic()
    time.sleep(max(0, target_rate - (time.monotonic() - loop_start)))


    # Ground station code, uncomment to use and comment the radio.send() and time.sleep(1) above
    # radio_message = radio.try_read()
    # if radio_message is not None:
    #     print("Radio RX {:3d}: {:3d}db: {:5}".format(packet_count, radio.rssi(), str(msg, 'ascii')))
    #     packet_count = packet_count + 1
