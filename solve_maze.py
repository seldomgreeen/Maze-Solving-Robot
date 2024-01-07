from zumo_2040_robot import motors
from zumo_2040_robot import robot
from zumo_2040_robot import imu
import time


motors = robot.Motors()
display = robot.Display()
yellow_led = robot.YellowLED()
encoders = robot.Encoders()
right = motors.right_motor_pwm
left = motors.left_motor_pwm
imu = robot.IMU()
imu.reset()
imu.enable_default()
proximity_sensors = robot.ProximitySensors()
rgb_leds = robot.RGBLEDs()
rgb_leds.set_brightness(3)

SENSOR_THRESHOLD = const(4)
TURN_SPEED_MAX = const(4000)
TURN_SPEED_MIN = const(1500)
# DECELERATION = const(150)
# ACCELERATION = const(150)
DIR_LEFT = const(0)
DIR_RIGHT = const(5)
sense_dir = DIR_RIGHT
turning_left = False
turning_right = False
turn_speed = TURN_SPEED_MAX
drive_motors = False

RGB_OFF = (0, 0, 0)
RGB_GREEN = (0, 255, 0)
RGB_YELLOW = (255, 64, 0)
RGB_RED = (255, 0, 0)


def updateScreen(text):
    display.fill(0)
    display.text(f"SciOly", 39, 0)
    display.text(f"Robot Tour", 24, 10)
    display.text(f"2023-2024", 0, 50)
    display.text(f"{text}", 0, 30)
    display.show()


updateScreen("")


def turn_left():
    left_speed = -2000
    right_speed = 2000

    initial_angle = 0
    # while initial_angle == 0:
    #    imu.gyro.read()
    #    initial_angle = imu.gyro.last_reading_dps[2]

    target_angle = initial_angle - 90

    while True:
        imu.gyro.read()
        turn_rate = imu.gyro.last_reading_dps[2]
        motors.set_speeds(left_speed + turn_rate, right_speed - turn_rate)

        if target_angle == -90:
            break

    #    if turn_rate <= target_angle:
    #        break
    if target_angle == initial_angle - 90:
        time.sleep(0.6)
        motors.set_speeds(0, 0)

def turn_right():
    left_speed = 2000
    right_speed = -2000

    initial_angle = 0
    # while initial_angle == 0:
    #    imu.gyro.read()
    #    initial_angle = imu.gyro.last_reading_dps[2]

    target_angle = initial_angle - 90

    while True:
        imu.gyro.read()
        turn_rate = imu.gyro.last_reading_dps[2]
        motors.set_speeds(left_speed + turn_rate, right_speed - turn_rate)

        if target_angle == -90:
            break

    #    if turn_rate <= target_angle:
    #        break
    if target_angle == initial_angle - 90:
        time.sleep(0.6)
        motors.set_speeds(0, 0)

def forwardInSeconds(seconds):
    start_time = time.time()
    while time.time() - start_time < seconds:
        motors.set_speeds(2000, 2000)
        time.sleep(0.1)
#    while True:
#    object_seen = object_detection()

#    if object_seen:
#        updateScreen("Object Detected")
#        set_front_rgb_leds(RGB_RED, RGB_RED, RGB_RED)
#        motors.set_speeds(0, 0)

#    else:
#        updateScreen("Starting")
#        set_front_rgb_leds(RGB_GREEN, RGB_GREEN, RGB_GREEN)
#        forward()
#    motors.set_speeds(0, 0)

def forward25():
    encoders.right_offset = 0
    encoders.left_offset = 0
    left, right = 0, 0
    motors.set_speeds(2000, 2000)
    while (left + right) < 3879:
        left, right = encoders.get_counts()
    motors.set_speeds(0, 0)

def forward():
    motors.set_speeds(2000, 2000)

def set_front_rgb_leds(front_left, front, front_right):
    rgb_leds.set(5, front_left)
    rgb_leds.set(4, front)
    rgb_leds.set(3, front_right)
    rgb_leds.show()

def object_detection():
    proximity_sensors.read()
    reading_front_left = proximity_sensors.front_counts_with_left_leds()
    reading_front_right = proximity_sensors.front_counts_with_right_leds()
    object_seen = any(
        reading > SENSOR_THRESHOLD
        for reading in (reading_front_left, reading_front_right)
    )

    if object_seen:
        return True
    else:
        return False

'''
while True:
    object_seen = object_detection()

    if object_seen:
        updateScreen("Object Detected")
        set_front_rgb_leds(RGB_RED, RGB_RED, RGB_RED)
        motors.set_speeds(0, 0)

    else:
        updateScreen("Starting")
        set_front_rgb_leds(RGB_GREEN, RGB_GREEN, RGB_GREEN)
        forward()
'''
'''
turn_left()
time.sleep(0.5)
forwardInSeconds(2)
time.sleep(0.5)
turn_right()
time.sleep(0.5)
forwardInSeconds(2)
'''