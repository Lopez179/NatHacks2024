import ICM_3D

class ICM_3D_I(ICM_3D):
  def __init__(self, bus, dev_add, start_reg, reg_scaler):
    super().__init__(self, bus, dev_add, start_reg, reg_scaler)

  @property
  def x(self):
    something = super().x
    print(f"Post super: {something}")