import smbus2
import time

I2C_BUS = 1
I2C_SLAVE_ADDRESS = 0x3E

bus = smbus2.SMBus(I2C_BUS)

try:
    while True:
        try:
            data = bus.read_i2c_block_data(I2C_SLAVE_ADDRESS, 0, 2)
            print(f"Data: {data}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)
except KeyboardInterrupt:
    bus.close()
    print("\nExiting...")
