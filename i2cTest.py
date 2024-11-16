import time

from smbus2 import SMBus



# Define the I2C bus (1 for Raspberry Pi 2 and later)
bus = SMBus(1)

# Define the I2C address of the ICM-20948
DEVICE_ADDRESS = 0x69

# Define register addresses
REG_BANK_SEL = 0x7F
PWR_MGMT_1 = 0x06
PWR_MGMT_2 = 0x07
GYRO_CONFIG_1 = 0x01
ACCEL_CONFIG = 0x14

# Define register bank values
USER_BANK_0 = 0x00
USER_BANK_2 = 0x20

# Define settings for accelerometer and gyroscope
GYRO_FS_SEL_2000DPS = 0x16  # Gyroscope: ±2000 dps, low-pass filter enabled
ACCEL_FS_SEL_16G = 0x18     # Accelerometer: ±16g

# Function to write a single register
def write_register(bus, address, register, value):
    bus.write_byte_data(address, register, value)

# Function to read a single register
def read_register(bus, address, register):
    return bus.read_byte_data(address, register)

# Function to select the user bank
def select_user_bank(bus, address, bank):
    write_register(bus, address, REG_BANK_SEL, bank)

# Main function to configure the ICM-20948
def configure_icm20948():
    # Step 1: Select User Bank 0
    select_user_bank(bus, DEVICE_ADDRESS, USER_BANK_0)

    # Step 2: Configure power management
    write_register(bus, DEVICE_ADDRESS, PWR_MGMT_1, 0x01)  # Enable PLL
    write_register(bus, DEVICE_ADDRESS, PWR_MGMT_2, 0x00)  # Enable Accel and Gyro

    # Step 3: Switch to User Bank 2
    select_user_bank(bus, DEVICE_ADDRESS, USER_BANK_2)

    # Step 4: Configure gyroscope and accelerometer
    write_register(bus, DEVICE_ADDRESS, GYRO_CONFIG_1, GYRO_FS_SEL_2000DPS)
    write_register(bus, DEVICE_ADDRESS, ACCEL_CONFIG, ACCEL_FS_SEL_16G)

    print("ICM-20948 configured to Mode 6 (Accel + Gyro Mode).")

    # Step 5: Verify the settings
    print("Verifying settings...")
    select_user_bank(bus, DEVICE_ADDRESS, USER_BANK_0)  # Return to User Bank 0 to verify power management
    pwr_mgmt_1 = read_register(bus, DEVICE_ADDRESS, PWR_MGMT_1)
    pwr_mgmt_2 = read_register(bus, DEVICE_ADDRESS, PWR_MGMT_2)

    select_user_bank(bus, DEVICE_ADDRESS, USER_BANK_2)  # Switch to User Bank 2 to verify sensor configs
    gyro_config_1 = read_register(bus, DEVICE_ADDRESS, GYRO_CONFIG_1)
    accel_config = read_register(bus, DEVICE_ADDRESS, ACCEL_CONFIG)

    # Output verification results
    print(f"PWR_MGMT_1: {hex(pwr_mgmt_1)} (Expected: 0x01)")
    print(f"PWR_MGMT_2: {hex(pwr_mgmt_2)} (Expected: 0x00)")
    print(f"GYRO_CONFIG_1: {hex(gyro_config_1)} (Expected: {hex(GYRO_FS_SEL_2000DPS)})")
    print(f"ACCEL_CONFIG: {hex(accel_config)} (Expected: {hex(ACCEL_FS_SEL_16G)})")


ACCEL_XOUT_H = 0x2D
ACCEL_XOUT_L = 0x2E
ACCEL_YOUT_H = 0x2F
ACCEL_YOUT_L = 0x30
ACCEL_ZOUT_H = 0x31
ACCEL_ZOUT_L = 0x32

GYRO_XOUT_H = 0x33
GYRO_XOUT_L = 0x34
GYRO_YOUT_H = 0x35
GYRO_YOUT_L = 0x36
GYRO_ZOUT_H = 0x37
GYRO_ZOUT_L = 0x38

REG_BANK_SEL = 0x7F
USER_BANK_0 = 0x00

# Scale factors for raw data conversion based on ±16g and ±2000dps settings
ACCEL_SCALE = 16.0 / 32768.0  # ±16g, 16-bit ADC
GYRO_SCALE = 2000.0 / 32768.0  # ±2000dps, 16-bit ADC

# Function to read two bytes and combine them into a signed 16-bit value
def read_signed_16(bus, address, high_reg, low_reg):
    high = read_register(bus, address, high_reg)
    low = read_register(bus, address, low_reg)
    value = (high << 8) | low
    # Convert to signed 16-bit
    return value if value < 32768 else value - 65536

# Function to read and print accelerometer and gyroscope data
def read_sensor_data():
    with SMBus(1) as bus:  # Use I2C bus 1
        # Step 1: Select User Bank 0
        select_user_bank(bus, DEVICE_ADDRESS, USER_BANK_0)

        # Step 2: Read accelerometer data
        accel_x = read_signed_16(bus, DEVICE_ADDRESS, ACCEL_XOUT_H, ACCEL_XOUT_L) * ACCEL_SCALE
        accel_y = read_signed_16(bus, DEVICE_ADDRESS, ACCEL_YOUT_H, ACCEL_YOUT_L) * ACCEL_SCALE
        accel_z = read_signed_16(bus, DEVICE_ADDRESS, ACCEL_ZOUT_H, ACCEL_ZOUT_L) * ACCEL_SCALE

        # Step 3: Read gyroscope data
        gyro_x = read_signed_16(bus, DEVICE_ADDRESS, GYRO_XOUT_H, GYRO_XOUT_L) * GYRO_SCALE
        gyro_y = read_signed_16(bus, DEVICE_ADDRESS, GYRO_YOUT_H, GYRO_YOUT_L) * GYRO_SCALE
        gyro_z = read_signed_16(bus, DEVICE_ADDRESS, GYRO_ZOUT_H, GYRO_ZOUT_L) * GYRO_SCALE

        # Step 4: Print the data
        print(f"Accelerometer (g): X={accel_x:.2f}, Y={accel_y:.2f}, Z={accel_z:.2f}")
        print(f"Gyroscope (dps): X={gyro_x:.2f}, Y={gyro_y:.2f}, Z={gyro_z:.2f}")


# Run the configuration
if __name__ == "__main__":
    configure_icm20948()

    # Main loop
    while True:
        read_sensor_data()
        # Sleep for a bit before reading again
        time.sleep(1)
