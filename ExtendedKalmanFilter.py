import numpy as np

class ExtendedKalmanFilter:
  def __init__(self, dt, process_noise, measurement_noise):
    """
    Initializes the Extended Kalman Filter for fusing accelerometer and gyroscope data.

    Parameters:
    - dt: Sampling time interval (s)
    - process_noise: Process noise covariance matrix (Q)
    - measurement_noise: Measurement noise covariance matrix (R)
    """
    self.dt = dt
    self.F = np.eye(6)  # State transition matrix
    self.F[0, 3] = self.F[1, 4] = self.F[2, 5] = dt  # Incorporate velocity integration

    self.Q = process_noise  # Process noise covariance matrix
    self.R = measurement_noise  # Measurement noise covariance matrix

    self.H = np.zeros((6, 6))  # Measurement matrix
    self.H[0, 0] = self.H[1, 1] = self.H[2, 2] = 1  # Position measurement
    self.H[3, 3] = self.H[4, 4] = self.H[5, 5] = 1  # Velocity measurement

    self.P = np.eye(6)  # Error covariance matrix
    self.state = np.zeros(6)  # State vector: [pos_x, pos_y, pos_z, vel_x, vel_y, vel_z]

  def predict(self):
    """
    Predict the next state based on the current state and model.
    """
    # Predict state
    self.state = self.F @ self.state

    # Predict error covariance
    self.P = self.F @ self.P @ self.F.T + self.Q

  def update(self, accel, gyro):
    """
    Update the state with new accelerometer and gyroscope measurements.

    Parameters:
    - accel: Corrected accelerometer measurements [ax, ay, az] in m/s^2.
    - gyro: Gyroscope measurements [gx, gy, gz] in rad/s.
    """
    # Gyroscope provides angular velocity; here, it can be used for orientation adjustments if needed.
    # For simplicity, we'll assume it's used indirectly via the process model.

    # Simulated measurements (integrated accel for velocity, position inferred from velocity)
    measured_velocity = np.array(accel) * self.dt
    measured_position = self.state[:3] + self.state[3:] * self.dt  # Integrate velocity for position

    
    # Combine position and velocity into a measurement vector
    z = np.hstack((measured_position, measured_velocity))

    # Compute innovation (difference between measured and predicted states)
    y = z - (self.H @ self.state)

    # Compute Kalman gain
    S = self.H @ self.P @ self.H.T + self.R
    K = self.P @ self.H.T @ np.linalg.inv(S)

    # Update state estimate
    self.state += K @ y

    # Update error covariance
    I = np.eye(len(self.state))
    self.P = (I - K @ self.H) @ self.P

    return self.state[:3], self.state[3:]  # Return position and velocity
