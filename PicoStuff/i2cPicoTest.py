import smbus2
import time
import RPi.GPIO as GPIO

I2C_BUS = 1
I2C_SLAVE_ADDRESS = 0x3E
SDA_PIN = 2  # GPIO 3 for SCL on the Raspberry Pi

bus = smbus2.SMBus(I2C_BUS)

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SDA_PIN, GPIO.OUT)

def reset_scl():
    # Reset the SCL line by toggling it
    GPIO.output(SDA_PIN, GPIO.LOW)
    time.sleep(0.01)  # Hold the line low for a short time
    GPIO.output(SDA_PIN, GPIO.HIGH)
    time.sleep(0.01)  # Let the clock line recover
    GPIO.setup(SDA_PIN, GPIO.IN)  # Reset the pin to input to allow I2C to resume

reset_scl()

if (False):
  try:
    while True:
        try:
            data = bus.read_i2c_block_data(I2C_SLAVE_ADDRESS, 0, 2)
            print(f"Data: {data}")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)
  except KeyboardInterrupt:
    bus.close()
    reset_scl()  # Reset the SCL pin on interrupt
    
    GPIO.cleanup()  # Clean up GPIO settings
    print("\nExiting...")
