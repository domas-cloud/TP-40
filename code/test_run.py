import serial, math, time

ser = serial.Serial('/dev/cu.usbmodem1101', 9600)

WHEEL_LENGTH = math.pi * 0.08

ENCODER_VALUE = 0
INITIAL_ANGLE = 0
DISTANCE_FROM_WALL = 30
DISTANCE_BETWEEN_SENSORS = 263
MAX_TURNING_ANGLE = 0

PROPORTIONAL_VALUE = 4
INTEGRAL_VALUE = 0

integral_value = 0
turning_angle = 0

def writeData():
    rot = 0 + round(turning_angle)
    ser.write(bytes(f"Rotate,{rot}\n", 'utf-8'))


while True:
    string = str(ser.readline())
    data = string.replace("b'", "").replace("\\n'", '').split(',')

    # Stabilizatorius, kad sektu pagal trumpiausia siena
    if len(data) == 5:
        f_front = int(data[0])
        f_left = int(data[1]) / 10 
        f_right = int(data[2]) / 10
        side_left = int(data[3]) / 10
        side_right = int(data[4]) / 10

        if True:
            # Tikslumas priklauso nuo ultrasonic informacijos
            y = (f_left - side_left)
            angle = math.atan( (y or 1) / DISTANCE_BETWEEN_SENSORS)
            distance = f_left * math.cos(angle)

            # PI Controller

            error = distance - DISTANCE_FROM_WALL
            integral_value += error
            #turning_angle = PROPORTIONAL_VALUE * error + INTEGRAL_VALUE * integral_value

            if abs(turning_angle) > MAX_TURNING_ANGLE:
                if turning_angle < 0:
                    turning_angle = -MAX_TURNING_ANGLE
                else:
                    turning_angle = MAX_TURNING_ANGLE

            print(data, distance, error, PROPORTIONAL_VALUE * error, INITIAL_ANGLE + round(turning_angle))

            if f_front < 70:
                turning_angle = 30


    if data[0].startswith("ENCODER"):
        ENCODER_VALUE = int(''.join(filter(str.isdigit, data[0])))

    writeData()
