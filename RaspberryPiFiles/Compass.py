import smbus
import time
import math
 
# HMC5883L register addresses
ADDRESS = 0x0D
CONFIG_A = 0x09
#CONFIG_B = 0x01
MODE = 0x01
X_MSB = 0x01
Z_MSB = 0x05
Y_MSB = 0x03

calibration_offset = [1.00, 1.00, 1.00] #(x_min - x_max)/2, (y_min - y_max)/2, (z_min - z_max)/2
#avg_delta = 	float avg_delta = (x_avg_delta + y_avg_
# delta + z_avg_delta) / 3;
#avg_delta / x_avg_delta, avg_delta / y_avg_delta, avg_delta / z_avg_delta
#Reference for calibration: https://www.appelsiini.net/2018/calibrate-magnetometer/
calibration_Scale = [0.96, 0.91, 1.16]
 
bus = smbus.SMBus(1)
 
def setup():
    #Settting QMCL 5883 to 512 OSR, 8G, 10Hz
    bus.write_byte_data(ADDRESS, 0x0B,0x01)
    bus.write_byte_data(ADDRESS, CONFIG_A, 0x1D)  # Set to 8 samples @ 15Hz
#    bus.write_byte_data(ADDRESS, CONFIG_B, 0x20)  # 1.3 gain LSb / Gauss 1090 (default)
#    bus.write_byte_data(ADDRESS, MODE, 0x00)  # Continuous measurement mode
 
def read_raw_data(addr):
    # Read raw 16-bit value
    high = bus.read_byte_data(ADDRESS, addr)
    low = bus.read_byte_data(ADDRESS, addr-1)
    
    # Combine them to get a 16-bit value
    value = (high << 8) + low
    if value > 32768:  # Adjust for 2's complement
        value = value - 65536
    return value
 
def compute_heading(x, y):
    # Calculate heading in radians
    heading_rad = math.atan2(y, x)
    
    # Adjust for declination angle (e.g. 0.0495 for ~2.8333 degrees)
    declination_angle = 0.0495
    heading_rad += declination_angle
    
    # Correct for when signs are reversed.
    if heading_rad < 0:
        heading_rad += 2 * math.pi
 
    # Check for wrap due to addition of declination.
    if heading_rad > 2 * math.pi:
        heading_rad -= 2 * math.pi
 
    # Convert radians to degrees for readability.
    heading_deg = heading_rad * (180.0 / math.pi)
    
    return heading_deg

def calibrate(x, y, z):
    x_cal = (x-calibration_offset[0])*calibration_Scale[0]
    y_cal = (y-calibration_offset[1])*calibration_Scale[1]
    z_cal = (z-calibration_offset[2])*calibration_Scale[2]
    return x_cal, y_cal, z_cal

def get_bearing():
    x = read_raw_data(X_MSB)
    y = read_raw_data(Y_MSB)
    z = read_raw_data(Z_MSB)
    x, y, z = calibrate(x,y,z)

    return compute_heading(x, y)

# def main():
#     setup()
    
#     while True:
#         x = read_raw_data(X_MSB)
#         y = read_raw_data(Y_MSB)
#         z = read_raw_data(Z_MSB)
#         x, y, z = calibrate(x,y,z)

#         heading = compute_heading(x, y)
        
#         print(f"X: {x:.2f} uT, Y: {y:.2f} uT, Z: {z:.2f} uT, Heading: {heading:.2f}°")
        
#         time.sleep(0.5)
 
# if __name__ == "__main__":
#     main()
