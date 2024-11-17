from collections import deque

class DriftCorrector:
  def __init__(self, window_size=50, threshold=0.01):
    """
    DriftCorrector dynamically estimates and corrects drift using a rolling average.

    Parameters:
    - window_size: The number of samples to calculate drift.
    - threshold: Minimum value to consider as drift (noise threshold).
    """
    self.window_size = window_size
    self.threshold = threshold
    self.x_drift = deque(maxlen=window_size)
    self.y_drift = deque(maxlen=window_size)
    self.z_drift = deque(maxlen=window_size)

  def update(self, raw_accel_x, raw_accel_y, raw_accel_z):
    """
    Update drift correction with new accelerometer readings.

    Parameters:
    - raw_accel_x, raw_accel_y, raw_accel_z: Raw accelerometer readings.

    Returns:
    - Corrected accelerometer values.
    """
    # Update drift estimation windows
    self.x_drift.append(raw_accel_x)
    self.y_drift.append(raw_accel_y)
    self.z_drift.append(raw_accel_z)

    # Calculate drift as the average of the window
    drift_x = sum(self.x_drift) / len(self.x_drift) if len(self.x_drift) > 0 else 0
    drift_y = sum(self.y_drift) / len(self.y_drift) if len(self.y_drift) > 0 else 0
    drift_z = sum(self.z_drift) / len(self.z_drift) if len(self.z_drift) > 0 else 0

    # Apply threshold filtering
    drift_x = drift_x if abs(drift_x) > self.threshold else 0
    drift_y = drift_y if abs(drift_y) > self.threshold else 0
    drift_z = drift_z if abs(drift_z) > self.threshold else 0

    # Subtract drift from raw values
    corrected_x = raw_accel_x - drift_x
    corrected_y = raw_accel_y - drift_y
    corrected_z = raw_accel_z - drift_z

    return corrected_x, corrected_y, corrected_z
