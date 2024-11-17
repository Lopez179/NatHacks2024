# **VR Hand Gesture Interface**

## **Project Overview**
Our project utilizes the **BioAmp EXG Pill** and an **accelerometer** to create a VR hand gesture interface, revolutionizing accessibility and interaction in virtual reality (VR) environments. This innovative solution is designed for individuals with mobility challenges, providing a **controller-less input method** that integrates seamlessly with any platform.

By bridging innovative hardware integration and advanced software design, our project aims to provide an alternative to existing user input devices. The result is a versatile, accessible, and intuitive tool that demonstrates the potential of wearable technology to make digital experiences more inclusive and engaging.

---

## **Features**
- **BioAmp EXG Integration**:
  - Captures high-fidelity biosignals for gesture recognition.
- **Accelerometer-Based Motion Tracking**:
  - Tracks hand motion in 3D space using the ICM-20948 sensor.
- **VR Compatibility**:
  - Translates gestures into inputs compatible with VR systems.
- **Controller-Less Design**:
  - Provides an alternative to traditional VR controllers for enhanced accessibility.
- **Real-Time Processing**:
  - Operates at high frequencies for seamless and responsive interaction.

---

## **Hardware Architecture**
1. **Raspberry Pi Pico**:
   - Serves as the **analog-to-digital converter** for the BioAmp EXG Pill’s output.
   - Acts as the signal acquisition unit, converting raw analog signals into digital data.
2. **Raspberry Pi 3**:
   - Processes the digital data from the Pico and integrates it with VR systems.
   - Handles motion tracking using the ICM-20948 sensor.

---

## **Software Requirements**
- **Python 3.7+**
- Required Libraries:
  - `smbus2` (I2C communication)
  - `numpy` (numerical computation)
  - `pynput` (mouse control)
  - `pyautogui` (optional for screen size detection)

---

## **Setup and Configuration**
### **1. Hardware Setup**
- Connect the **BioAmp EXG Pill** to the Raspberry Pi Pico for signal acquisition.
- Connect the **ICM-20948 accelerometer** to the Raspberry Pi 3 via I2C.
- Ensure proper wiring for power and data communication between the Pico and Pi.

### **2. Software Installation**
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
2. Install required libraries:
    ```bash
    pip install smbus2 numpy pynput pyautogui
3. Sensor Configuration:
- Run config.py to initialize the accelerometer with appropriate settings.
4. Verify I2C Communication:
- Use quick_test.py to validate I2C communication with the sensors.

## **Usage**
### **1. Gesture Tracking**
- Run `i2cTest.py` to start the interface.
- Follow on-screen instructions to calibrate and use the system.

### **2. Motion-Based Actions**
- Customize predefined actions in `output.py` for gesture-to-action mapping.

### **3. Position Tracking**
- Use `ICM_3D_I.py` to track hand position in 3D space.

---

## **Example Applications**
### **VR Accessibility**
- Enables individuals with limited mobility to interact with VR environments.

### **Wearable Technology**
- Showcases the potential of wearable devices for intuitive input.

### **Gaming**
- Adds immersive gesture-based controls for VR games.

---

## **Testing**
### **1. System Tests**
- Validate gesture detection and motion tracking using `i2cTest.py`.

### **2. Quick Tests**
- Use `quick_test.py` to check individual sensor communication.

### **3. Debugging**
- Use `scaner_test.py` for detailed I2C testing.

---

## **Future Enhancements**
- Add support for machine learning-based gesture recognition.
- Integrate with additional VR platforms and APIs.
- Optimize processing for higher sampling rates and lower latency.

---

## **Contributors**
- Ohm Panchal
- Vishit Soni
- Leander Lopez
- Weston Mcclinchey
- Steven Sager
- Abdullah Sherwani
