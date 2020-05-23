# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO

from SpotifyController import SpotifyController
from FFTDisplay import FFTDisplay

PREV_PIN = 23
START_PAUSE_PIN = 24
NEXT_PIN = 25

FFT_PIN_ANO = [ 4,  5,  6,  7,  8,  9, 10, 11] 
FFT_PIN_CAT = [12, 13, 14, 15, 16, 17, 18, 19] 

GPIO.setmode(GPIO.BCM)

def main():
  SpotifyController(PREV_PIN, START_PAUSE_PIN, NEXT_PIN)
  display = FFTDisplay(FFT_PIN_ANO, FFT_PIN_CAT)

  try:
    print('start...')
    while True:
      display.outputWave()

  except KeyboardInterrupt:
    pass
  except Exception as err:
    print(err)

  del display
  GPIO.cleanup()

if __name__ == '__main__':
  main()

