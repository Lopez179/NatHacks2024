from reg_func import *
import time
from collections import deque

class ICM_3D:
  def __init__(self, bus, dev_add, start_reg, sample_rate, reg_scaler, window = 0x04, threshold = 0):
    self.x_h_reg = start_reg
    self.x_l_reg = start_reg +1
    self.y_h_reg = start_reg +2
    self.y_l_reg = start_reg +3
    self.z_h_reg = start_reg +4
    self.z_l_reg = start_reg +5
    self.scaler = reg_scaler
    self.samp_rate = sample_rate
    self.dev = dev_add
    self.bus = bus

    self.window = window
    self.threshold = threshold
    self.x_hist = deque(maxlen=self.window)
    self.y_hist = deque(maxlen=self.window)
    self.z_hist = deque(maxlen=self.window)


    self.calibrate()

  @property
  def x(self):
    #print(f"x : {self.scaler * (read_signed_16(self.bus, self.dev, self.x_h_reg, self.x_l_reg))} | {self.scaler * (read_signed_16(self.bus, self.dev, self.x_h_reg, self.x_l_reg)) - self.x_tare}")
    return self.apply_filter(self.scaler * (read_signed_16(self.bus, self.dev, self.x_h_reg, self.x_l_reg)) - self.x_tare, self.x_hist)
     
  @property
  def y(self):
    return self.apply_filter(self.scaler * (read_signed_16(self.bus, self.dev, self.y_h_reg, self.y_l_reg)) - self.y_tare, self.y_hist)
    
  @property
  def z(self):
    return self.apply_filter(self.scaler * (read_signed_16(self.bus, self.dev, self.z_h_reg, self.z_l_reg)) - self.z_tare, self.z_hist)
    
  def calibrate(self):
    num_samples = 0x40
    self.x_tare = 0
    self.y_tare = 0
    self.z_tare = 0

    #p_x = 0
    #p_y = 0
    #p_z = 0

    #self.x_drift = 0
    #self.y_drift = 0
    #self.z_drift = 0

    for _ in range(num_samples):
      x = self.scaler * (read_signed_16(self.bus, self.dev, self.x_h_reg, self.x_l_reg))
      self.x_tare += x
      #self.x_drift += x - p_x
      #p_x = x

      y = self.scaler * (read_signed_16(self.bus, self.dev, self.y_h_reg, self.y_l_reg))
      self.y_tare += y
      #self.y_drift += y - p_y
      #p_y = y
      
      z = self.scaler * (read_signed_16(self.bus, self.dev, self.z_h_reg, self.z_l_reg))
      self.z_tare += z
      #self.z_drift += z - p_z
      #p_z = z

      time.sleep(self.samp_rate)

    self.x_tare //= num_samples
    self.y_tare //= num_samples
    self.z_tare //= num_samples

    #self.x_drift //= num_samples
    #self.y_drift //= num_samples
    #self.z_drift //= num_samples

    print(f"Calibrated Tare Values: X={self.x_tare:.2f}, Y={self.y_tare:.2f}, Z={self.z_tare:.2f}")
    #print(f"Calibrated Drift Values: X={self.x_drift:.2f}, Y={self.y_drift:.2f}, Z={self.z_drift:.2f}")

  def apply_filter(self, raw_value, history):
    if abs(raw_value) <= self.threshold: raw_value = 0  
    history.append(raw_value)

    return sum(history) / len(history) if len(history) == self.window else raw_value

  def __str__(self):
    return f"X={self.x:.2f}, Y={self.y:.2f}, Z={self.z:.2f}"

