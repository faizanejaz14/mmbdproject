import time
import RPi.GPIO as gpio
import Compass as compass

# Motor + Odometry Logic
# declare the sensor and led pin
sensor_pin = 31

revs = 10
turn_speed = 100
threshold = 500

motor1_in1 = 13
motor1_in2 = 15

motor2_in1 = 12
motor2_in2 = 16

motor3_in1 = 18
motor3_in2 = 22

motor4_in1 = 36
motor4_in2 = 11

right_enables = 32
left_enables = 33

compass_init = 0
# IR_sensor = 23

# left_enables =
# right_enables =

gpio.setwarnings(False)

gpio.cleanup()

print("Setting Up")
gpio.setmode(gpio.BOARD)
gpio.setup(motor1_in1, gpio.OUT)
gpio.setup(motor1_in2, gpio.OUT)
gpio.setup(motor2_in1, gpio.OUT)
gpio.setup(motor2_in2, gpio.OUT)
gpio.setup(motor3_in1, gpio.OUT)
gpio.setup(motor3_in2, gpio.OUT)
gpio.setup(motor4_in1, gpio.OUT)
gpio.setup(motor4_in2, gpio.OUT)

# gpio.setup(all_enables, gpio.OUT)

gpio.setup(sensor_pin, gpio.IN)

# speed = gpio.PWM(all_enables, 1000)
# speed.start(25)
# gpio.setup(IR_sensor, gpio.IN)

gpio.setup(left_enables, gpio.OUT)
gpio.setup(right_enables, gpio.OUT)

speed_left = gpio.PWM(left_enables, 1000)
speed_right = gpio.PWM(right_enables, 1000)
speed_left.start(100)
speed_right.start(100)


def reset():
    gpio.output(motor1_in1, gpio.LOW)
    gpio.output(motor1_in2, gpio.LOW)
    gpio.output(motor2_in1, gpio.LOW)
    gpio.output(motor2_in2, gpio.LOW)
    gpio.output(motor3_in1, gpio.LOW)
    gpio.output(motor3_in2, gpio.LOW)
    gpio.output(motor4_in1, gpio.LOW)
    gpio.output(motor4_in2, gpio.LOW)


def golgol():
    #    speed.ChangeDutyCycle(75)
    gpio.output(motor1_in1, gpio.HIGH)
    gpio.output(motor1_in2, gpio.LOW)
    gpio.output(motor2_in1, gpio.HIGH)
    gpio.output(motor2_in2, gpio.LOW)
    gpio.output(motor3_in1, gpio.HIGH)
    gpio.output(motor3_in2, gpio.LOW)
    gpio.output(motor4_in1, gpio.HIGH)
    gpio.output(motor4_in2, gpio.LOW)


def turn_90_degrees():
    print(compass.get_bearing())
    if 85 < abs(compass.get_bearing() - compass_init) < 95:  # +- 5 degrees
        return False  # right turn complete
    return True  # Keep making turn


def left():
    while turn_90_degrees():
        #        speed.ChangeDutyCycle(15)
        gpio.output(motor1_in1, gpio.HIGH)
        gpio.output(motor1_in2, gpio.LOW)
        gpio.output(motor2_in1, gpio.HIGH)
        gpio.output(motor2_in2, gpio.LOW)
        gpio.output(motor3_in1, gpio.LOW)
        gpio.output(motor3_in2, gpio.HIGH)
        gpio.output(motor4_in1, gpio.LOW)
        gpio.output(motor4_in2, gpio.HIGH)
        time.sleep(1)
#        speed.ChangeDutyCycle(25)


def right():
    while turn_90_degrees():
     #       speed.ChangeDutyCycle(15)
        gpio.output(motor1_in1, gpio.LOW)
        gpio.output(motor1_in2, gpio.HIGH)
        gpio.output(motor2_in1, gpio.LOW)
        gpio.output(motor2_in2, gpio.HIGH)
        gpio.output(motor3_in1, gpio.HIGH)
        gpio.output(motor3_in2, gpio.LOW)
        gpio.output(motor4_in1, gpio.HIGH)
        gpio.output(motor4_in2, gpio.LOW)
        time.sleep(1)
 #       speed.ChangeDutyCycle(25)


def forward():
 #   speed.ChangeDutyCycle(turn_speed)
    gpio.output(motor1_in1, gpio.LOW)
    gpio.output(motor1_in2, gpio.HIGH)
    gpio.output(motor2_in1, gpio.HIGH)
    gpio.output(motor2_in2, gpio.LOW)
    gpio.output(motor3_in1, gpio.HIGH)
    gpio.output(motor3_in2, gpio.LOW)
    gpio.output(motor4_in1, gpio.LOW)
    gpio.output(motor4_in2, gpio.HIGH)


def backward():
  #  speed.ChangeDutyCycle(turn_speed)
    gpio.output(motor1_in1, gpio.HIGH)
    gpio.output(motor1_in2, gpio.LOW)
    gpio.output(motor2_in1, gpio.LOW)
    gpio.output(motor2_in2, gpio.HIGH)
    gpio.output(motor3_in1, gpio.LOW)
    gpio.output(motor3_in2, gpio.HIGH)
    gpio.output(motor4_in1, gpio.HIGH)
    gpio.output(motor4_in2, gpio.LOW)


def odom(ir_prev):
    counter1 = 0  # revs count
    counter2 = 0  # similar reading in ir count
    while (True):
        ir_new = gpio.input(sensor_pin)
        if ir_new != ir_prev:
            counter2 += 1
        if counter2 == threshold:
            counter2 = 0
            counter1 += 1
            ir_prev = ir_new
            print(counter1)

        if counter1 == revs:
            break
    print(counter1)


def main():
    # Initializing Compass
    compass.setup()

    try:
        print("\n")
        print("The default speed & direction of motor is LOW & Forward.....")
        print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
        print("\n")

        while (1):
            x = input("input move:")

            if x == 's':
                print("stop")
                reset()
                x = 'z'

            elif x == 'r':
                compass_init = compass.get_bearing()
                print("right")
                right()
                # odom()
                reset()
                x = 'z'

            elif x == 'f':
                print("forward")
                ir_prev = gpio.input(sensor_pin)
                forward()
                odom(ir_prev)
                reset()
                x = 'z'

            elif x == 'l':
                compass_init = compass.get_bearing()
                print("left")
                left()
                # odom()
                reset()
                x = 'z'

            elif x == 'g':
                print("golgol")
                golgol()
                time.sleep(3)
                reset()
                x = 'z'

            elif x == 'b':
                print("backward")
                ir_prev = gpio.input(sensor_pin)
                backward()
                odom(ir_prev)
                reset()
                x = 'z'

            elif x == '1':
                print("SLOW")
                # speed.ChangeDutyCycle(25)
                x = 'z'

            elif x == 'e':
                gpio.cleanup()
                break

            else:
                print("<<<  wrong data  >>>")
                print("please enter the defined data to continue.....")
    except KeyboardInterrupt:
        gpio.cleanup()


if __name__ == "__main__":
    main()
