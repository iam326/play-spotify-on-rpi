# -*- coding: utf-8 -*-
import pyaudio
import numpy as np

"""
[参考]
https://note.com/mokuichi/n/n70d61237e6c7
https://tam5917.hatenablog.com/entry/2019/04/28/125857
"""

RATE = 22000 # 22kHz
CHUNK = 1024

class FFTGenerator():
  def __init__(self):
    self.audio = pyaudio.PyAudio()
    self.stream = self.audio.open(format=pyaudio.paInt16,
                             channels=1,
                             rate=RATE,
                             input=True,
                             output=False,
                             frames_per_buffer=CHUNK)

  def __del__(self):
    self.stream.stop_stream()
    self.stream.close()
    self.audio.terminate()

  def is_active(self):
    return self.stream.is_active()

  def read(self):
    input = self.stream.read(CHUNK, exception_on_overflow=False)
    ndarray = np.frombuffer(input, dtype='int16') / 32768
    fft = np.fft.fft(ndarray)
    fft = np.abs(fft) ** 2
    fft = fft[0:int(CHUNK / 2)]
    return 20 * np.log10(fft + 0.0001)

if __name__ == '__main__':
  fft = FFTGenerator()

  try:
    while True:
      if fft.is_active():
        print(fft.read())
  except KeyboardInterrupt:
    pass

  del fft

