# -*- coding: utf-8 -*-
import os
import RPi.GPIO as GPIO

from Spotify import Spotify

class SpotifyController():
  def __init__(self, prev_pin, start_pause_pin, next_pin):
    self.prev_pin = prev_pin
    self.start_pause_pin = start_pause_pin
    self.next_pin = next_pin

    client_id = os.environ['SPOTIPY_CLIENT_ID']
    client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
    redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
    username = os.environ['SPOTIPY_USERNAME']
    scope = 'user-read-playback-state,user-modify-playback-state'
    self.spotify = Spotify(client_id, client_secret, redirect_uri, username, scope)

    self.device_id = self.spotify.find_device_id('raspotify')
    if self.device_id == None:
      raise Exception('target device not found')

    self.setupPins()

  def setupPins(self):
    for pin in [self.prev_pin, self.start_pause_pin, self.next_pin]:
      GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
      GPIO.add_event_detect(pin, GPIO.RISING, callback=self.handleEvent, bouncetime=200)

  def handleEvent(self, ch):
    if ch == self.prev_pin:
      print('prev track')
      self.spotify.prev_track(device_id=self.device_id)
    elif ch == self.start_pause_pin:
      print('start or pause track')
      self.spotify.toggle_start_pause(device_id=self.device_id)
    elif ch == self.next_pin:
      print('next track')
      self.spotify.next_track(device_id=self.device_id)

if __name__ == '__main__':
  from time import sleep

  GPIO.setmode(GPIO.BCM)

  try:
    SpotifyController(23, 24, 25)
    print('wait...')
    while True:
      sleep(0.1)
  except KeyboardInterrupt:
    pass

  GPIO.cleanup()

