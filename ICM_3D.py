from reg_func import *

class ICM_3D:
  def __init__(self, bus, dev_add, start_reg, reg_scaler):
    self.x_h_reg = start_reg
    self.x_l_reg = start_reg +1
    self.y_h_reg = start_reg +2
    self.y_l_reg = start_reg +3
    self.z_h_reg = start_reg +4
    self.z_l_reg = start_reg +5
    self.scaler = reg_scaler
    self.dev = dev_add
    self.bus = bus

    self.x_tare = self.x
    self.y_tare = self.y
    self.z_tare = self.z

  @property
  def x(self):
    return self.scaler * (read_signed_16(self.bus, self.dev, self.x_h_reg, self.x_l_reg) - self.x_tare)
  
  @property
  def y(self):
    return self.scaler * (read_signed_16(self.bus, self.dev, self.y_h_reg, self.y_l_reg) - self.y_tare)
    
  @property
  def z(self):
    return self.scaler * (read_signed_16(self.bus, self.dev, self.y_h_reg, self.y_l_reg) - self.z_tare)
    
  def print(self):
    print(f"X={self.x:.2f}, Y={self.y:.2f}, Z={self.z:.2f}")

