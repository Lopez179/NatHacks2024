from reg_func import *

# Main function to configure the ICM-20948
def configure_icm20948(bus ,DEVICE_ADDRESS):
  # Define settings for accelerometer and gyroscope
  GYRO_FS_SEL_2000DPS = 0x16  # Gyroscope: ±2000 dps, low-pass filter enabled
  ACCEL_FS_SEL_16G = 0x18   # Accelerometer: ±16g

  # Define register bank values
  REG_BANK_SEL = 0x7F
  USER_BANK_0 = 0x00
  USER_BANK_2 = 0x20
  USER_BANK_3 = 0x30

  # Define register addresses
  PWR_MGMT_1 = 0x06
  PWR_MGMT_2 = 0x07
  GYRO_CONFIG_1 = 0x01
  ACCEL_CONFIG = 0x14

  # Step 1: Select User Bank 0
  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_0)

  # Step 2: Configure power management
  write_register(bus, DEVICE_ADDRESS, PWR_MGMT_1, 0x01)  # Enable PLL
  write_register(bus, DEVICE_ADDRESS, PWR_MGMT_2, 0x00)  # Enable Accel and Gyro

  # Step 3: Switch to User Bank 2
  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_2)

  # Step 5: Switch to User Bank 3 to configure the magnetometer
  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_3)

  # Step 4: Configure gyroscope and accelerometer
  write_register(bus, DEVICE_ADDRESS, GYRO_CONFIG_1, GYRO_FS_SEL_2000DPS)
  write_register(bus, DEVICE_ADDRESS, ACCEL_CONFIG, ACCEL_FS_SEL_16G)

  print("ICM-20948 configured to Mode 6 (Accel + Gyro Mode).")

  # Step 5: Verify the settings
  print("Verifying settings...")
  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_0)  # Return to User Bank 0 to verify power management
  pwr_mgmt_1 = read_register(bus, DEVICE_ADDRESS, PWR_MGMT_1)
  pwr_mgmt_2 = read_register(bus, DEVICE_ADDRESS, PWR_MGMT_2)

  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_2)  # Switch to User Bank 2 to verify sensor configs
  gyro_config_1 = read_register(bus, DEVICE_ADDRESS, GYRO_CONFIG_1)
  accel_config = read_register(bus, DEVICE_ADDRESS, ACCEL_CONFIG)

  # Output verification results
  print(f"PWR_MGMT_1: {hex(pwr_mgmt_1)} (Expected: 0x01)")
  print(f"PWR_MGMT_2: {hex(pwr_mgmt_2)} (Expected: 0x00)")
  print(f"GYRO_CONFIG_1: {hex(gyro_config_1)} (Expected: {hex(GYRO_FS_SEL_2000DPS)})")
  print(f"ACCEL_CONFIG: {hex(accel_config)} (Expected: {hex(ACCEL_FS_SEL_16G)})")