from smbus2 import SMBus
import time

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
ACCEL_FS_SEL_16G = 0x18   # Accelerometer: ±16g

# Function to select the user bank
def select_user_bank(bus, address, bank):
  write_register(bus, address, REG_BANK_SEL, bank)

# Function to write a single register
def write_register(bus, address, register, value):
  bus.write_byte_data(address, register, value)

# Function to read a single register
def read_register(bus, address, register):
  return bus.read_byte_data(address, register)

def read_signed_16(bus, dev_add, high_reg, low_reg):
  return (lambda val : val if val < 32768 else val - 65536)((read_register(bus, dev_add, high_reg) << 8) | read_register(bus, dev_add, low_reg))

class ICM_3D:
  def __init__(self, dev_add, start_reg, reg_scaler):
    self.x_h_reg = start_reg
    self.x_l_reg = start_reg +1
    self.y_h_reg = start_reg +2
    self.y_l_reg = start_reg +3
    self.z_h_reg = start_reg +4
    self.z_l_reg = start_reg +5
    self.scaler = reg_scaler
    self.dev = dev_add

  @property
  def x(self):
    return self.scaler * read_signed_16(bus, self.dev, self.x_h_reg, self.x_l_reg)
  
  @property
  def y(self):
    return self.scaler * read_signed_16(bus, self.dev, self.y_h_reg, self.y_l_reg)
    
  @property
  def z(self):
    return self.scaler * read_signed_16(bus, self.dev, self.y_h_reg, self.y_l_reg)
    
  def print(self):
    print(f"X={self.x:.2f}, Y={self.y:.2f}, Z={self.z:.2f}")

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

def read_sensor_data():
  select_user_bank(bus, DEVICE_ADDRESS, USER_BANK_0)

  accel = ICM_3D(DEVICE_ADDRESS, 0x2D, 16.0 / 32768.0)
  gyro = ICM_3D(DEVICE_ADDRESS, 0x33, 2000.0 / 32768.0)

  print(f"Accelerometer (g): {accel.print()}")
  print(f"Gyroscope (dps): {gyro.print()}")


# Run the configuration
if __name__ == "__main__":
  configure_icm20948()

  # Main loop
  while True:
    read_sensor_data()
    # Sleep for a bit before reading again
    time.sleep(1)
