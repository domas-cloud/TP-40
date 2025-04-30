import serial  # Bendraujama per serial (USB) su mikrovaldikliu (pvz., Arduino)
import math    # Matematinės funkcijos (trigonometrinės, pi ir kt.)
import time    # Laiko valdymui (jei reikėtų sleep ar laiko žymų)

# Atidarome serial ryšį su įrenginiu (nurodytas prievadas ir greitis)
ser = serial.Serial('/dev/cu.usbmodem1101', 9600)

# Rato ilgis (apskritimo ilgis) – naudojamas greičiui/skaičiavimams
WHEEL_LENGTH = math.pi * 0.08  # Ratas 8 cm skersmens

# Pradinės reikšmės
ENCODER_VALUE = 0             # Vertė, gauta iš enkoderio
INITIAL_ANGLE = 0             # Pradinis pasukimo kampas
DISTANCE_FROM_WALL = 30       # Idealus atstumas nuo sienos (cm)
DISTANCE_BETWEEN_SENSORS = 263  # Atstumas tarp šoninių jutiklių (mm)
MAX_TURNING_ANGLE = 0         # Maksimalus leidžiamas pasukimo kampas (ribojamas)

# PI kontrolerio konstantos
PROPORTIONAL_VALUE = 4
INTEGRAL_VALUE = 0

# Integralinė reikšmė PI kontroleriui (kaupiama paklaida)
integral_value = 0
turning_angle = 0  # Apskaičiuotas pasukimo kampas

# Funkcija siunčia duomenis į mikrovaldiklį per serial – posūkio komandą
def writeData():
    rot = 0 + round(turning_angle)  # Apskaičiuojamas kampas suapvalinant
    ser.write(bytes(f"Rotate,{rot}\n", 'utf-8'))  # Siunčiama per UART: "Rotate,30"

# Pagrindinis ciklas – nuolatinis duomenų skaitymas ir apdorojimas
while True:
    # Nuskaitomi duomenys iš serial jungties (string formatu)
    string = str(ser.readline())
    
    # Pašalinami nereikalingi simboliai ir išskaidoma į atskirus matavimus
    data = string.replace("b'", "").replace("\\n'", '').split(',')

    # Tikriname, ar gauti visi 5 laukeliai (priekinis + 4 šoniniai)
    if len(data) == 5:
        f_front = int(data[0])           # Atstumas priekyje
        f_left = int(data[1]) / 10       # Ultragarso kairėje (pataisyta skalė cm)
        f_right = int(data[2]) / 10      # Ultragarso dešinėje
        side_left = int(data[3]) / 10    # Šoninis kairėje
        side_right = int(data[4]) / 10   # Šoninis dešinėje

        # Kampo skaičiavimas pagal skirtumą tarp dviejų jutiklių
        y = (f_left - side_left)  # Skirtumas tarp priekinio ir šoninio kairio jutiklio
        angle = math.atan((y or 1) / DISTANCE_BETWEEN_SENSORS)  # Apskaičiuojamas pasvirimo kampas
        distance = f_left * math.cos(angle)  # Atstumas nuo sienos, pataisytas pagal kampą

        # PI kontroleris: apskaičiuojamas klaidos dydis
        error = distance - DISTANCE_FROM_WALL
        integral_value += error

        # (užkomentuota) Tikslus kampo skaičiavimas su PI kontrole
        # turning_angle = PROPORTIONAL_VALUE * error + INTEGRAL_VALUE * integral_value

        # Ribojame, kad pasukimo kampas neviršytų maksimalios leidžiamos vertės
        if abs(turning_angle) > MAX_TURNING_ANGLE:
            if turning_angle < 0:
                turning_angle = -MAX_TURNING_ANGLE
            else:
                turning_angle = MAX_TURNING_ANGLE

        # Išvedama diagnostinė informacija: matavimai, klaida, korekcija, kampas
        print(data, distance, error, PROPORTIONAL_VALUE * error, INITIAL_ANGLE + round(turning_angle))

        # Jei priekyje kliūtis ar siena arti, sukame
        if f_front < 70:
            turning_angle = 30  # Sukame 30 laipsnių

    # Jei ateina ENCODER duomenys (judėjimo jutiklio info)
    if data[0].startswith("ENCODER"):
        ENCODER_VALUE = int(''.join(filter(str.isdigit, data[0])))  # Ištraukiamas skaičius

    # Išsiunčiame sukimosi komandą į mikrovaldiklį
    writeData()
