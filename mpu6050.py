from machine import I2C

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Пробуждаем датчик от спящего режима
        self.i2c.writeto_mem(self.addr, 0x6B, bytes([0]))

    def _read_word(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        val = (data[0] << 8) | data[1]
        return val - 65536 if val > 32767 else val

    def get_accel(self):
        # Чтение ускорений по осям X, Y, Z в g (±2g диапазон)
        ax = self._read_word(0x3B) / 16384.0
        ay = self._read_word(0x3D) / 16384.0
        az = self._read_word(0x3F) / 16384.0
        return ax, ay, az