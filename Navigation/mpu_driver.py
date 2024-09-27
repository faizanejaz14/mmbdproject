import time
import RPi.GPIO as gpio
import mpu6050
import math

mpu = mpu6050.mpu6050(0x68)

threshold = 500

sensor_pin = 31
motor1_in1 = 13
motor1_in2 = 15

motor2_in1 = 12
motor2_in2 = 16

motor3_in1 = 18
motor3_in2 = 22

motor4_in1 = 36
motor4_in2 = 11

left_enables = 33
right_enables = 32
turn_delay = 1

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

gpio.setup(sensor_pin, gpio.IN)

gpio.setup(left_enables, gpio.OUT)
gpio.setup(right_enables, gpio.OUT)

speed_left = gpio.PWM(left_enables, 1000)
speed_right = gpio.PWM(right_enables, 1000)
speed_left.start(40)
speed_right.start(30)


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
    global turn_delay
    init_angle = mpu.get_gyro_data()['x']
    #    speed.ChangeDutyCycle(75)
    gpio.output(motor1_in1, gpio.HIGH)
    gpio.output(motor1_in2, gpio.LOW)
    gpio.output(motor2_in1, gpio.HIGH)
    gpio.output(motor2_in2, gpio.LOW)
    gpio.output(motor3_in1, gpio.HIGH)
    gpio.output(motor3_in2, gpio.LOW)
    gpio.output(motor4_in1, gpio.HIGH)
    gpio.output(motor4_in2, gpio.LOW)
    time.sleep(1)
    final_angle = mpu.get_gyro_data()['x']
    turn_delay = 90/(final_angle - init_angle)
    print(turn_delay)


def left():
    global turn_delay
    gpio.output(motor1_in1, gpio.HIGH)
    gpio.output(motor1_in2, gpio.LOW)
    gpio.output(motor2_in1, gpio.HIGH)
    gpio.output(motor2_in2, gpio.LOW)
    gpio.output(motor3_in1, gpio.LOW)
    gpio.output(motor3_in2, gpio.HIGH)
    gpio.output(motor4_in1, gpio.LOW)
    gpio.output(motor4_in2, gpio.HIGH)
    time.sleep(turn_delay)


def right():
 #   speed.ChangeDutyCycle(turn_speed)
    global turn_delay
    gpio.output(motor1_in1, gpio.LOW)
    gpio.output(motor1_in2, gpio.HIGH)
    gpio.output(motor2_in1, gpio.LOW)
    gpio.output(motor2_in2, gpio.HIGH)
    gpio.output(motor3_in1, gpio.HIGH)
    gpio.output(motor3_in2, gpio.LOW)
    gpio.output(motor4_in1, gpio.HIGH)
    gpio.output(motor4_in2, gpio.LOW)
    time.sleep(turn_delay)


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


def smh(ir_prev, revs):
    global speed_left
    global speed_right
    initial_angle = mpu.get_gyro_data()['x']
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
            # print(counter1)
        if abs(mpu.get_gyro_data()['x'] - initial_angle) > 10:
            temp = speed_right
            speed_right = speed_left
            speed_left = temp
            time.sleep(1)
            print(mpu.get_gyro_data()['x'])
        if counter1 == revs:
            break


def calibrate_timer():
    golgol()
    reset()


def go_straight(value):
    revs = 2 * int(value/((3*math.pi)/50))
    ir_prev = gpio.input(sensor_pin)
    forward()
    smh(ir_prev, revs)
    reset()

# def u_turn():


def run_driver(action, value):
    try:
        if action == "right" or action == "east":
            right()
            go_straight(value)
            reset()
            action = 'z'

        elif action == "left" or "west":
            left()
            go_straight(value)
            reset()
            action = 'z'

        elif action == "north":
            go_straight(value)
            reset()
            action = 'z'

        # elif action == "south":

    except KeyboardInterrupt:
        gpio.cleanup()
