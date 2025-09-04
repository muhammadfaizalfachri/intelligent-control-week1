import cv2
import numpy as np

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ================= Warna Merah (2 range, dipersempit supaya tidak kena kulit)
    lower_red1 = np.array([0, 150, 120])   # Naikkan S dan V agar kulit tidak terdeteksi
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 150, 120])
    upper_red2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red1, upper_red1) | cv2.inRange(hsv, lower_red2, upper_red2)

    # ================= Warna Hijau
    lower_green = np.array([35, 100, 100])
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # ================= Warna Biru
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # ================= Deteksi kontur untuk masing-masing warna
    def detect_and_label(mask, color_name, box_color):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # filter biar tidak noise kecil
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
                cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, box_color, 2)

    # Panggil fungsi untuk tiap warna
    detect_and_label(mask_red, "Merah", (0, 0, 255))
    detect_and_label(mask_green, "Hijau", (0, 255, 0))
    detect_and_label(mask_blue, "Biru", (255, 0, 0))

    # ✅ Tampilkan frame asli dengan kotak + label
    cv2.imshow("Deteksi Warna (Merah, Hijau, Biru)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
