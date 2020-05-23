# -*- coding: utf-8 -*-
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spotify():
  def __init__(self, client_id, client_secret, redirect_uri, username, scope):
    self.oauth = SpotifyOAuth(client_id=client_id,
                              client_secret=client_secret,
                              redirect_uri=redirect_uri,
                              username=username,
                              scope=scope)
    self.play_state = False

    with open('./secrets.json', 'r') as f:
      self.secrets = json.load(f)

    access_token = self.refresh_access_token()
    self.app = spotipy.Spotify(auth=access_token)

  def refresh_access_token(self):
    new_tokens = self.oauth.refresh_access_token(self.secrets['refresh_token'])
    if self.secrets['refresh_token'] != new_tokens['refresh_token']:
      with open('./secrets.json', 'w') as f:
        self.secrets['refresh_token'] = new_tokens['refresh_token']
        json.dump(self.secrets, f)

    return new_tokens['access_token']

  def find_device_id(self, device_name):
    devices = self.app.devices()
    target_device_id = None
    for dev in devices['devices']:
      if dev['name'].startswith(device_name):
        target_device_id = dev['id']
        break

    return target_device_id

  def next_track(self, device_id):
    self.app.next_track(device_id=device_id)

  def prev_track(self, device_id):
    self.app.previous_track(device_id=device_id)

  def toggle_start_pause(self, device_id):
    if not self.play_state:
      self.app.start_playback(device_id=device_id)
    else:
      self.app.pause_playback(device_id=device_id)
    self.play_state = not self.play_state

if __name__ == '__main__':
  import os

  client_id = os.environ['SPOTIPY_CLIENT_ID']
  client_secret = os.environ['SPOTIPY_CLIENT_SECRET']
  redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
  username = os.environ['SPOTIPY_USERNAME']
  scope = 'user-read-playback-state,user-modify-playback-state'

  spotify = Spotify(client_id, client_secret, redirect_uri, username, scope)
  print(spotify.find_device_id('raspotify'))

