from smbus2 import SMBus
import time

from reg_func import *
from config import *
from ICM_3D import ICM_3D
from ICM_3D_I import ICM_3D_I
from output import *

if __name__ == "__main__":
  bus = SMBus(1)

  DEVICE_ADDRESS = 0x69
  configure_icm20948(bus, DEVICE_ADDRESS)

  REG_BANK_SEL = 0x7F
  USER_BANK_0 = 0x00
  sample_rate = 0.01
  reset_period = 100
  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_0)

  accel = ICM_3D_I(bus, DEVICE_ADDRESS, 0x2D, sample_rate, 16.0 / 32768.0)
  #gyro = ICM_3D(bus, DEVICE_ADDRESS, 0x33, sample_rate, 2000.0 / 32768.0)
  OutputHelper = PreDefinedMovements()
  input()
  counter = 0
  while True:
    responses = ""
    if (accel.y > 1.7):
      responses = responses + "X"
      OutputHelper.move_right()
    elif (accel.y < -1.7):
      responses = responses + "-X"
      OutputHelper.move_left()

    if (accel.x > 1.7):
      responses = responses + "Y"
      OutputHelper.move_up()
    elif (accel.x < -1.7):
      responses = responses + "-Y"
      OutputHelper.move_down()
    
    print(responses)

    counter += 1
    time.sleep(sample_rate)

    if counter >= reset_period:
      counter = 0
      accel.reset()
