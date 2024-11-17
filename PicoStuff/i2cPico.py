import smbus2
import time

# I2C Bus and Slave Address
I2C_BUS = 1  # Adjust to match your Raspberry Pi's I2C bus
I2C_SLAVE_ADDRESS = 0x3E  # Slave address of the Pico

# Create an I2C bus instance
bus = smbus2.SMBus(I2C_BUS)

def read_adc_from_slave():
    try:
        # Read 2 bytes from the slave
        data = bus.read_i2c_block_data(I2C_SLAVE_ADDRESS, 0, 2)
        # Combine the two bytes into a single 16-bit value
        adc_value = (data[0] << 8) | data[1]
        return adc_value
    except Exception as e:
        print(f"Error reading from slave: {e}")
        return None

def main():
    print("Starting I2C master")
    while True:
        adc_value = read_adc_from_slave()
        if adc_value is not None:
            print(f"Received ADC value: {adc_value}")
        time.sleep(1)  # Poll every second

if __name__ == "__main__":
    main()
