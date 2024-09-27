import time
import RPi.GPIO as gpio

motor1_in1 = 13
motor1_in2 = 15

motor2_in1 = 12
motor2_in2 = 16

motor3_in1 = 18
motor3_in2 = 22

motor4_in1 = 36
motor4_in2 = 11

all_enables = 32

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

gpio.setup(all_enables,gpio.OUT)

speed = gpio.PWM(all_enables, 1000)
speed.start(25)
# gpio.setup(IR_sensor, gpio.IN)

# speed_left = gpio.PWM(left_enables, 1000)
# speed_right = gpio.PWM(right_enables, 1000)
# speed_left.start(25)
# speed_right.start(25)


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


def left():
    #    speed.ChangeDutyCycle(75)
    gpio.output(motor1_in1, gpio.LOW)
    gpio.output(motor1_in2, gpio.HIGH)
    gpio.output(motor2_in1, gpio.HIGH)
    gpio.output(motor2_in2, gpio.LOW)
    gpio.output(motor3_in1, gpio.LOW)
    gpio.output(motor3_in2, gpio.HIGH)
    gpio.output(motor4_in1, gpio.HIGH)
    gpio.output(motor4_in2, gpio.LOW)


def right():
    #    speed.ChangeDutyCycle(75)
    gpio.output(motor1_in1, gpio.HIGH)
    gpio.output(motor1_in2, gpio.LOW)
    gpio.output(motor2_in1, gpio.LOW)
    gpio.output(motor2_in2, gpio.HIGH)
    gpio.output(motor3_in1, gpio.HIGH)
    gpio.output(motor3_in2, gpio.LOW)
    gpio.output(motor4_in1, gpio.LOW)
    gpio.output(motor4_in2, gpio.HIGH)


def forward():
 #   speed.ChangeDutyCycle(75)
    gpio.output(motor1_in1, gpio.LOW)
    gpio.output(motor1_in2, gpio.HIGH)
    gpio.output(motor2_in1, gpio.HIGH)
    gpio.output(motor2_in2, gpio.LOW)
    gpio.output(motor3_in1, gpio.HIGH)
    gpio.output(motor3_in2, gpio.LOW)
    gpio.output(motor4_in1, gpio.LOW)
    gpio.output(motor4_in2, gpio.HIGH)


def backward():
 #   speed.ChangeDutyCycle(75)
    gpio.output(motor1_in1, gpio.HIGH)
    gpio.output(motor1_in2, gpio.LOW)
    gpio.output(motor2_in1, gpio.LOW)
    gpio.output(motor2_in2, gpio.HIGH)
    gpio.output(motor3_in1, gpio.LOW)
    gpio.output(motor3_in2, gpio.HIGH)
    gpio.output(motor4_in1, gpio.HIGH)
    gpio.output(motor4_in2, gpio.LOW)

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
                right()
                time.sleep(3)
                reset()
                x = 'z'

            elif x == 'f':
                print("forward")
                forward()
                time.sleep(3)
                reset()
                x = 'z'

            elif x == 'l':
                print("left")
                left()
                time.sleep(3)
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
                backward()
                time.sleep(3)
                reset()
                x = 'z'

            elif x == '1':
                print("SLOW")
                speed.ChangeDutyCycle(25)
                x = 'z'

                
            elif x == '2':
                print("medium")
                speed.ChangeDutyCycle(50)
                x = 'z'
            
            
            elif x == '3':
                print("fast")
                speed.ChangeDutyCycle(75)
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