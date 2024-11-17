from smbus2 import SMBus
import time
from reg_func import *
from config import *
from ICM_3D import ICM_3D
from DriftCorrector import DriftCorrector
from ExtendedKalmanFilter import ExtendedKalmanFilter
import numpy as np
from output import *

if __name__ == "__main__":
  bus = SMBus(1)
  DEVICE_ADDRESS = 0x69

  configure_icm20948(bus, DEVICE_ADDRESS)

  REG_BANK_SEL = 0x7F
  USER_BANK_0 = 0x00
  sample_rate = 0.01
  dt = 16
  select_user_bank(bus, DEVICE_ADDRESS, REG_BANK_SEL, USER_BANK_0)

  input("Calibrate")
  accel = ICM_3D(bus, DEVICE_ADDRESS, 0x2D, sample_rate, 16.0 / 32768.0)
  gyro = ICM_3D(bus, DEVICE_ADDRESS, 0x33, sample_rate, 2000.0 / 32768.0)

  drift_corrector = DriftCorrector(window_size=8, threshold=0)

  # EKF setup
  process_noise = np.diag([1e-4, 1e-4, 1e-4, 1e-3, 1e-3, 1e-3])
  measurement_noise = np.diag([1e-2, 1e-2, 1e-2, 1e-1, 1e-1, 1e-1])
  ekf = ExtendedKalmanFilter(dt, process_noise, measurement_noise)

  input("Run")
  thres = 0.3
  OutputHelper = PreDefinedMovements()
  counter = 0
  while True:
    current_time = time.time()

    # Read accelerometer and gyroscope data
    accel_data = (accel.x, accel.y, accel.z)
    gyro_data = (gyro.x, gyro.y, gyro.z)

    # Correct accelerometer drift
    corrected_accel = drift_corrector.update(*accel_data)

    # Update EKF
    position, velocity = ekf.update(corrected_accel, gyro_data)

    #responses = ""
    if (velocity[1] < thres):
      #responses = responses + "X"
      OutputHelper.move_right()
    elif (velocity[1] > -thres):
      #responses = responses + "-X"
      OutputHelper.move_left()
    if (velocity[0] > thres):
      #responses = responses + "Y"
      OutputHelper.move_up()
    elif (velocity[0] < -thres):
      #responses = responses + "-Y"
      OutputHelper.move_down()
    
    #print(responses)
    counter += 1
    if (0x400 < counter):
      print("reset")
      ekf.state = np.zeros(6)
      counter = 0
    #print(f"Position (m): X={position[0]:.2f}, Y={position[1]:.2f}, Z={position[2]:.2f}")
    #print(f"Velocity (m/s): X={velocity[0]:.2f}, Y={velocity[1]:.2f}, Z={velocity[2]:.2f}")

    time.sleep(sample_rate)

