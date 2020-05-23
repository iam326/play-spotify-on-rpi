import RPi.GPIO as GPIO
import numpy as np
from math import ceil
from time import sleep

from FFTGenerator import FFTGenerator

class FFTDisplay():
  def __init__(self, pin_ano, pin_cat):
    self.pin_row = pin_ano
    self.pin_col = pin_cat
    self.row_length = len(self.pin_row)
    self.col_length = len(self.pin_col)
    # 8x8 の配列を生成する
    self.matrix = [[False] * self.row_length for i in range(self.col_length)]
    self.fft = FFTGenerator()
    self.setupPins()

  def __del__(self):
    self.resetPins()
    del self.fft

  def setupPins(self):
    for row in self.pin_row:
      GPIO.setup(row, GPIO.OUT, initial=GPIO.LOW)

    for col in self.pin_col:
      GPIO.setup(col, GPIO.OUT, initial=GPIO.HIGH)

  def resetPins(self):
    for row in self.pin_row:
      GPIO.output(row, GPIO.LOW)

    for col in self.pin_col:
      GPIO.output(col, GPIO.HIGH)

  def readWave(self):
    # len(wave) == 512
    wave = self.fft.read()
    # 64 個ずつに要素を分け、それぞれの平均値を計算する
    wave = np.mean(wave.reshape(-1, 64), axis=1)
    # 小数点を切り捨てる
    return np.rint(wave)

  def level(self, val):
    # val は -80 ~ 80 の範囲の値
    # -60 ~ 20 の値を 1 ~ 8 で段階分けする
    # -61 より下の値は 0 とする
    # 0 以上の値は 8 とする
    lev = ceil((val + 60) / 10)
    # ↓ だと ~60 ~ 0 を 8段階で分ける
    # lev = ceil((val + 60) / 7.5)
    if lev > self.row_length:
      lev = self.row_length
    elif lev < 0:
      lev = 0
    return lev

  def updateMatrix(self, wave):
    for i in range(len(wave)):
      lev = self.level(wave[i])
      col = [False] * self.row_length
      for j in range(lev):
        col[j] = True
      # COL は逆から値を入れていく (PIN を入れ替えるのが面倒なため)
      self.matrix[self.col_length - 1 - i] = col

  def outputWave(self):
    wave = self.readWave()
    self.updateMatrix(wave)

    for col in range(self.col_length):
      for row in range(self.row_length):
        if self.matrix[col][row] == True:
          GPIO.output(self.pin_col[col], GPIO.LOW)
          GPIO.output(self.pin_row[row], GPIO.HIGH)
        sleep(0.00001)
        GPIO.output(self.pin_col[col], GPIO.HIGH)
        GPIO.output(self.pin_row[row], GPIO.LOW)

if __name__ == '__main__':
  pin_ano = [ 4,  5,  6,  7,  8,  9, 10, 11] 
  pin_cat = [12, 13, 14, 15, 16, 17, 18, 19]

  GPIO.setmode(GPIO.BCM)

  try:
    display = FFTDisplay(pin_ano, pin_cat)
    while True:
      display.outputWave()
  except KeyboardInterrupt:
    pass
  except Exception as err:
    print(err)
    pass

  del display
  GPIO.cleanup()

