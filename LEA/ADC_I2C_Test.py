import smbus
import time

# I²C bus number (usually 1 on Raspberry Pi)
I2C_BUS = 1
# I²C address of the Pico
ADC_ADDRESS = 0x12

# Create an SMBus instance
bus = smbus.SMBus(I2C_BUS)

def read_adc_value():
    # Request 2 bytes from the Pico
    adc_raw_data = bus.read_i2c_block_data(ADC_ADDRESS, 0, 2)
    # Combine the two bytes into a single 16-bit value
    adc_value = (adc_raw_data[0] << 8) | adc_raw_data[1]
    return adc_value

try:
    while True:
        adc_value = read_adc_value()
        print(f"ADC Value: {adc_value}")
        time.sleep(1)  # Wait for 1 second before the next read
except KeyboardInterrupt:
    print("Program terminated.")
