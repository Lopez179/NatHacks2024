import smbus
import time

bus = smbus.SMBus(1)  # Raspberry Pi I2C bus 1

def scan_i2c():
  for address in range(0x03, 0x77):
    try:
      bus.write_byte(address, 0)
      print(f"Device found at address 0x{address:02X}")
    except:
      pass

scan_i2c()
