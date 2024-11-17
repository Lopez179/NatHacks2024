from smbus2 import SMBus

MAGNETOMETER_I2C_ADDR = 0x0C
MAG_WIA = 0x00  # Who Am I register

try:
    bus = SMBus(1)
    who_am_i = bus.read_byte_data(MAGNETOMETER_I2C_ADDR, MAG_WIA)
    print(f"Magnetometer WHO_AM_I register: 0x{who_am_i:X}")
except OSError as e:
    print(f"Error accessing magnetometer: {e}")