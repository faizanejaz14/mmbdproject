import time
import RPi.GPIO as gpio
import mpu6050

mpu = mpu6050.mpu6050(0x68)
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

# all_enables = 32

# IR_sensor = 23

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

# gpio.setup(all_enables, gpio.OUT)

gpio.setup(sensor_pin, gpio.IN)

# speed = gpio.PWM(all_enables, 1000)
# speed.start(25)
# gpio.setup(IR_sensor, gpio.IN)


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


def smh(ir_prev):
    global speed_left
    global speed_right
    counter1 = 0  # revs count
    counter2 = 0  # similar reading in ir count
    initial_angle = mpu.get_gyro_data()['x']
    print(initial_angle)
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
        if abs(mpu.get_gyro_data()['x'] - initial_angle) > 10:
            temp = speed_right
            speed_right = speed_left
            speed_left = temp
            time.sleep(1)
            print(mpu.get_gyro_data()['x'])
    print(counter1)


def main():
    print("MAIN GAME")
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
                print("right")
                # ir_prev = gpio.input(sensor_pin)
                right()
                # smh(ir_prev)
                reset()
                x = 'z'

            elif x == 'f':
                print("forward")
                ir_prev = gpio.input(sensor_pin)
                forward()
                smh(ir_prev)
                reset()
                x = 'z'

            elif x == 'l':
                print("left")
                # ir_prev = gpio.input(sensor_pin)
                left()
                # smh(ir_prev)
                reset()
                x = 'z'

            elif x == 'g':
                print("golgol")
                # ir_prev = gpio.input(sensor_pin)
                golgol()
                # smh(ir_prev)
                reset()
                x = 'z'

            elif x == 'b':
                print("backward")
                ir_prev = gpio.input(sensor_pin)
                backward()
                smh(ir_prev)
                reset()
                x = 'z'

            elif x == '1':
                print("SLOW")
#                speed.ChangeDutyCycle(25)
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
