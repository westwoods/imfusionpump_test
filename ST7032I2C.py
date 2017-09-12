import smbus, time

class ST7032I(object):

  def __init__(self, addr, i2c_chan, **init_kws):
    self.addr, self.bus = addr, smbus.SMBus(i2c_chan)
    self.init(**init_kws)

  def _write(self, data, cmd=0, delay=None):
    self.bus.write_i2c_block_data(self.addr, cmd, list(data))
    if delay: time.sleep(delay)

  def init(self, contrast=0x3F, icon=False, booster=False):
    assert contrast < 0x40 # 6 bits only, probably not used on most lcds
    pic_high = 0b0111 << 4 | (contrast & 0x0f) # c3 c2 c1 c0
    pic_low = ( 0b0101 << 4 |
      icon << 3 | booster << 2 | ((contrast >> 4) & 0x03) ) # c5 c4
    self._write([0x38, 0x39, 0x14, pic_high, pic_low, 0x6c], delay=0.01)
    self._write([0x0c, 0x01, 0x06], delay=0.01)

  def move(self, row=0, col=0):
    assert 0 <= row <= 1 and 0 <= col <= 15, [row, col]
    self._write([0b1000 << 4 | (0x40 * row + col)])

  def addstr(self, chars, pos=None):
    if pos is not None:
      row, col = (pos, 0) if isinstance(pos, int) else pos
      self.move(row, col)
    self._write(map(ord, chars), cmd=0x40)

  def clear(self):
    self._write([0x01])

if __name__ == '__main__':
  lcd = ST7032I(0x3e, 1)
  while True:
    ts_tuple = time.localtime()
    lcd.clear()
    lcd.addstr(time.strftime('date: %y-%m-%d', ts_tuple), 0)
    lcd.addstr(time.strftime('time: %H:%M:%S', ts_tuple), 1)
    time.sleep(1)
