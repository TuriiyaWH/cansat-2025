import board
import busio
import sdcardio
import storage
import os
import time

class SDStorage:
    def __init__(self, spi_sck=board.GP10, spi_mosi=board.GP11, spi_miso=board.GP12, cs=board.GP15):
        """Initialize SD card and mount it."""
        spi = busio.SPI(spi_sck, spi_mosi, spi_miso)
        self.sdcard = sdcardio.SDCard(spi, cs)
        self.vfs = storage.VfsFat(self.sdcard)
        storage.mount(self.vfs, "/sd")  # Mount SD card at "/sd"
        print("SD card mounted successfully.")
        # Use a fixed log filename and clear it
        self.log_filename = "/sd/cansat_log.txt"
        self.clear_log()

    def clear_log(self, filename=None):
        """Clear the contents of the log file."""
        if filename is None:
            filename = self.log_filename
        try:
            with open(filename, "w") as file:  # 'w' mode overwrites the file
                file.write("")  # Clear file contents
            print(f"Cleared log file: {filename}")
        except OSError as e:
            print(f"Error clearing file {filename}: {e}")

    def write_log(self, data, filename=None):
        """
        Append data to the log file.
        If filename is not provided, use the default self.log_filename.
        """
        if filename is None:
            filename = self.log_filename
        try:
            with open(filename, "a") as file:
                file.write(data + "\n")
                file.flush()  # Ensure data is written immediately
                os.sync()
            #print(f"Data logged to {filename}: {data}")
        except OSError as e:
            print(f"Error writing to SD card: {e}")

    def read_log(self):
        """Read data from the log file."""
        if filename is None:
            filename = self.log_filename
        try:
            with open(self.log_filename, "r") as file:
                return file.readlines()
        except OSError as e:
            print(f"Error reading SD card: {e}")
            return None

def is_sd_responsive():
    try:
        # Try writing a temporary file
        with open("/sd/temp.txt", "w") as f:
            f.write("test")
        # Try reading it back
        with open("/sd/temp.txt", "r") as f:
            content = f.read()
        # Clean up the temporary file
        os.remove("/sd/temp.txt")
        return content == "test"
    except OSError:
        return False
