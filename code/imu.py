import time
import board
import busio
import adafruit_bno055
import math

class BNO055_IMU:
    def __init__(self, i2c_bus):
        self.sensor = adafruit_bno055.BNO055_I2C(i2c_bus)
        self.calibrated = False

    def get_orientation(self):
        """Returns roll, pitch, and yaw (heading) in degrees."""
        yaw, roll, pitch = self.sensor.euler  # BNO055 outputs in (heading, roll, pitch)
        return {
            "roll": roll if roll is not None else 0.0,
            "pitch": pitch if pitch is not None else 0.0,
            "yaw": yaw if yaw is not None else 0.0  # Heading
        }

    def get_acceleration(self):
        """Returns acceleration in m/s² for x, y, and z axes."""
        ax, ay, az = self.sensor.acceleration
        return {
            "ax": ax if ax is not None else 0.0,
            "ay": ay if ay is not None else 0.0,
            "az": az if az is not None else 0.0
        }

    def get_magnetometer(self):
        """Returns magnetometer readings in microteslas for x, y, and z axes."""
        mx, my, mz = self.sensor.magnetic
        return {
            "mx": mx if mx is not None else 0.0,
            "my": my if my is not None else 0.0,
            "mz": mz if mz is not None else 0.0
        }

    def is_calibrated(self):
        """Checks if the IMU is fully calibrated."""
        sys_cal, gyro_cal, accel_cal, mag_cal = self.sensor.calibration_status
        self.calibrated = sys_cal == 3 and gyro_cal == 3 and accel_cal == 3 and mag_cal == 3
        return {
            "system": sys_cal,
            "gyro": gyro_cal,
            "accelerometer": accel_cal,
            "magnetometer": mag_cal,
            "fully_calibrated": self.calibrated
        }

    def calibrate(self):
        """Guides the user through calibration if the IMU is not fully calibrated."""
        while not self.calibrated:
            status = self.is_calibrated()
            print(f"Calibration status: {status}")
            time.sleep(1)
        print("BNO055 is fully calibrated!")

if __name__ == "__main__":
    i2cimu = busio.I2C(board.GP7, board.GP6)  # Modify according to your setup     i2c = busio.I2C(board.SCL, board.SDA)
    imu = BNO055_IMU(i2cimu)

    while True:
        orientation = imu.get_orientation()
        acceleration = imu.get_acceleration()
        magnetometer = imu.get_magnetometer()
        calibration = imu.is_calibrated()

        print(f"Orientation: {orientation}")
        print(f"Acceleration: {acceleration}")
        print(f"Magnetometer: {magnetometer}")
        print(f"Calibration: {calibration}")
        print("-----------------------------")
        time.sleep(1)
