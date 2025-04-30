import cv2
import numpy as np

# HSV spalvų ribos žaliai (pagal tavo piniginę)
green_lower = np.array([83, 100, 150])
green_upper = np.array([97, 160, 230])

# HSV spalvų ribos raudonai (padalinta į dvi dalis dėl HSV cikliškumo)
red_lower1 = np.array([0, 120, 70])
red_upper1 = np.array([10, 255, 255])
red_lower2 = np.array([170, 120, 70])
red_upper2 = np.array([180, 255, 255])

# Kuri spalva kurioje zonoje turi būti
desired_zone = {
    'red': 'right',   # raudonas objektas turi būti dešinėje
    'green': 'left'   # žalias objektas turi būti kairėje
}

# Neutralios zonos plotis aplink centro liniją
BUFFER = 75          # pusė neutralios zonos pločio (viso 150px)
TOLERANCE = 10       # leidžiama paklaida zonoje

# Įjungiame kamerą
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Kamera nerasta")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Kadro aukštis ir plotis
    h, w = frame.shape[:2]
    center = w // 2
    left_bound = center - BUFFER
    right_bound = center + BUFFER

    # Konvertuojame į HSV spalvų erdvę
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Sukuriame kaukes raudonai spalvai (dvi zonos HSV skalėje)
    mask_r1 = cv2.inRange(hsv, red_lower1, red_upper1)
    mask_r2 = cv2.inRange(hsv, red_lower2, red_upper2)
    mask_red = cv2.bitwise_or(mask_r1, mask_r2)

    # Kaukė žaliai spalvai
    mask_green = cv2.inRange(hsv, green_lower, green_upper)

    detection = None

    # Tikriname kiekvieną spalvą atskirai
    for color, mask in [('red', mask_red), ('green', mask_green)]:
        conts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not conts:
            continue

        # Pasirenkame didžiausią kontūrą (didžiausias objektas)
        c = max(conts, key=cv2.contourArea)
        if cv2.contourArea(c) < 300:
            continue  # ignoruojame mažus triukšmus

        # Skaičiuojame objekto centroidą
        M = cv2.moments(c)
        if M['m00'] == 0:
            continue
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Nubraižome kontūrą ir spalvos pavadinimą
        cv2.drawContours(frame, [c], -1, (255, 255, 255), 2)
        cv2.putText(frame, color, (cx - 20, cy - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Zonų nustatymas pagal bounding box kraštus
        x, y, w_box, h_box = cv2.boundingRect(c)
        left_edge = x
        right_edge = x + w_box

        # Nustatome, kurioje zonoje yra objektas
        if right_edge < left_bound - TOLERANCE:
            zone = 'left'
        elif left_edge > right_bound + TOLERANCE:
            zone = 'right'
        else:
            zone = 'neutral'

        detection = (color, zone)
        break  # tik vienas objektas vienu metu

    if detection:
        color, zone = detection
        target = desired_zone[color]

        # Komandos logika
        if zone == target:
            command = 'STOP'
        elif zone == 'neutral':
            command = 'GO_LEFT' if target == 'left' else 'GO_RIGHT'
        elif zone == 'left':
            command = 'GO_RIGHT'
        else:
            command = 'GO_LEFT'

        print(f"{color} objektas → zona: {zone} → {command}")
    else:
        print("Nerasta objekto")

    # Nubraižomos zonos ant vaizdo
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (left_bound, h), (0, 0, 255), -1)         # Kairė zona (raudona)
    cv2.rectangle(overlay, (left_bound, 0), (right_bound, h), (128, 128, 128), -1)  # Neutralioji (pilka)
    cv2.rectangle(overlay, (right_bound, 0), (w, h), (0, 255, 0), -1)        # Dešinė zona (žalia)
    frame = cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)  # permatomas sluoksnis

    # Parodomas rezultatas lange
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF in (ord('q'), 27):  # paspaudus 'q' arba ESC – išeiti
        break

# Išvalome resursus
cap.release()
cv2.destroyAllWindows()
