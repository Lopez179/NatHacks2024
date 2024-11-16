from smbus2 import SMBus
import time

from reg_func import *
from config import *
import ICM_3D


if __name__ == "__main__":
  bus = SMBus(1)

  DEVICE_ADDRESS = 0x69
  configure_icm20948(bus, DEVICE_ADDRESS)

  REG_BANK_SEL = 0x7F
  USER_BANK_0 = 0x00
  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_0)

  while True:
    accel = ICM_3D(DEVICE_ADDRESS, 0x2D, 16.0 / 32768.0)
    gyro = ICM_3D(DEVICE_ADDRESS, 0x33, 2000.0 / 32768.0)

    print(f"Accelerometer (g): {accel.print()}")
    print(f"Gyroscope (dps): {gyro.print()}")

    time.sleep(1)
