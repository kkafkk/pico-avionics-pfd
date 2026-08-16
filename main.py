from machine import Pin, I2C
import time
import math
import ssd1306
import mpu6050

# Светодиоды
led_green = Pin(14, Pin.OUT)
led_red = Pin(15, Pin.OUT)

# Шины I2C
i2c_mpu = I2C(0, sda=Pin(4), scl=Pin(5), freq=100000)
mpu = mpu6050.MPU6050(i2c_mpu)

i2c_oled = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

CX, CY = 64, 32

def draw_aircraft_symbol():
    # Центральная точка прицела
    oled.fill_rect(CX - 1, CY - 1, 3, 3, 1)
    
    # Крылья самолета (жирные планки с окантовкой)
    oled.fill_rect(CX - 24, CY - 1, 14, 3, 1)
    oled.fill_rect(CX + 11, CY - 1, 14, 3, 1)
    
    # Вертикальные законцовки крыльев
    oled.vline(CX - 24, CY + 2, 4, 1)
    oled.vline(CX + 24, CY + 2, 4, 1)
    
    # Носовой киль
    oled.vline(CX, CY - 6, 4, 1)

def draw_pfd(pitch, roll):
    roll_rad = math.radians(roll)
    tan_r = math.tan(roll_rad)
    cos_r = math.cos(roll_rad)
    sin_r = math.sin(roll_rad)

    # Смещение горизонта по тангажу
    pitch_y = CY + int(pitch * 0.8)

    # 1. Заливка земли штриховкой / сплошным под линией горизонта
    for x in range(0, 128, 2):
        # Вычисляем Y точки горизонта для текущего X
        y_horiz = int(pitch_y + (x - CX) * tan_r)
        if y_horiz < 64:
            y_start = max(0, y_horiz)
            # Шахматная штриховка "земли"
            for y in range(y_start, 64, 2):
                oled.pixel(x + (y % 4 == 0), y, 1)

    # 2. Основная белая линия горизонта
    x0, y0 = 0, int(pitch_y - CX * tan_r)
    x1, y1 = 127, int(pitch_y + (127 - CX) * tan_r)
    oled.line(max(0, min(127, x0)), max(0, min(63, y0)),
              max(0, min(127, x1)), max(0, min(63, y1)), 1)

    # 3. Шкала тангажа (лесенки Pitch Ladders +15° и -15°)
    for deg in (-15, 15):
        h_offset = int((pitch + deg) * 0.8)
        bar_cy = CY + h_offset
        bx = int(10 * cos_r)
        by = int(10 * sin_r)
        
        px0 = CX - bx - int(h_offset * sin_r)
        py0 = bar_cy + int(h_offset * cos_r) - h_offset
        px1 = CX + bx - int(h_offset * sin_r)
        py1 = bar_cy - int(h_offset * cos_r) - h_offset

        if 0 <= py0 < 64 and 0 <= py1 < 64:
            oled.line(px0, py0, px1, py1, 1)

    # 4. Неподвижный силуэт самолётика поверх горизонта
    draw_aircraft_symbol()

    # 5. Боковые панели параметров
    oled.rect(0, 0, 26, 12, 1)
    oled.text(f"{int(pitch):+2d}", 3, 2)

    oled.rect(102, 0, 26, 12, 1)
    oled.text(f"{int(roll):+2d}", 105, 2)

print("Запуск реалистичного авиагоризонта...")

while True:
    try:
        ax, ay, az = mpu.get_accel()
        pitch = math.atan2(ax, math.sqrt(ay**2 + az**2)) * 57.2958
        roll = math.atan2(ay, math.sqrt(ax**2 + az**2)) * 57.2958

        oled.fill(0)
        draw_pfd(pitch, roll)

        # Контроль критических углов
        if abs(pitch) > 30 or abs(roll) > 30:
            led_green.value(0)
            led_red.value(1)
        else:
            led_green.value(1)
            led_red.value(0)

        oled.show()
        time.sleep(0.02)

    except Exception as e:
        time.sleep(0.04)