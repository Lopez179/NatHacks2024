from ICM_3D import ICM_3D

class ICM_3D_I(ICM_3D):
  def __init__(self, bus, dev_add, start_reg, sample_rate, reg_scaler):
    super().__init__(bus, dev_add, start_reg, sample_rate, reg_scaler)
    self.x_val = 0
    self.y_val = 0
    self.z_val = 0

    self._x_val = 0
    self._y_val = 0
    self._z_val = 0

  @property
  def _x(self):
    self._x_val += 0.5 * (self.x + self.x_val) * self.samp_rate
    self.x_val = self.x
    return self._x_val
  
  @property
  def _y(self):
    self._y_val += 0.5 * (self.y + self.y_val) * self.samp_rate
    self.y_val = self.y
    return self._y_val
  
  @property
  def _z(self):
    self._z_val += 0.5 * (self.z + self._z_val) * self.samp_rate
    self.z_val = self.z
    return self._z_val

  def __str__(self):
    return f"{super().__str__()} | _X={self._x:.2f}, _Y={self._y:.2f}, _Z={self._z:.2f}"