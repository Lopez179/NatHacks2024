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
    return super().x
  
  @property
  def _y(self):
    return super().x
  
  @property
  def _z(self):
    return super().x

  @property
  def x(self):
    self.x_val += 0.5 * (self._x + self._x_val) * self.samp_rate
    self._x_val = self._x
    return self.x_val
  
  @property
  def y(self):
    self.y_val += 0.5 * (self._y + self._y_val) * self.samp_rate
    self._y_val = self._y
    return self.y_val
  
  @property
  def z(self):
    self.z_val += 0.5 * (self._z + self._z_val) * self.samp_rate
    self._z_val = self._z
    return self.z_val