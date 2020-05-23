# -*- coding: utf-8 -*-
import os
import json
import RPi.GPIO as GPIO
from time import sleep
from json.decoder import JSONDecodeError

import spotipy
# import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth

"""
export SPOTIPY_USERNAME='xxx'
export SPOTIPY_CLIENT_ID='yyy'
export SPOTIPY_CLIENT_SECRET='zzz'
export SPOTIPY_REDIRECT_URI='http://...'
"""

NEXT = 23
START_STOP = 24
PREV = 25
PLAY_STATE = False

username = os.environ['SPOTIPY_USERNAME']
scope = 'user-read-playback-state,user-modify-playback-state'

"""
try:
  # http://sakanaaas.hateblo.jp/entry/2017/07/02/122740
  # 本来であればここでブラウザが起動する
  # 認証確認をOKした後に遷移するページのURLをターミナルに貼り付けることで
  # tokenを取得することができる

  # が、SSHでRaspberry Piに接続している場合、ブラウザを起動できず、ここで処理が止まる
  # 一時的な対応方法として、Mac側にて同じ認証方法でtokenを取得すると生成されるファイル
  # .cache-{username} を、このファイルが存在するディレクトリにコピーすると、
  # tokenの有効期限が切れるまでは、ここの処理を通すことができる

  # 有効期限が切れてもtokenを更新して継続的にアクセスできるようにするためには、
  # このコメントアウトより後段の方法で認証を行う必要がある
  token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
  # https://github.com/plamere/spotipy/issues/176#issuecomment-307632735
  # 変なキャッシュが残ることが原因で?認証に失敗するバグへの対応
  os.remove('.cache-' + username)
  token = util.prompt_for_user_token(username, scope)
sp = spotipy.Spotify(auth=token)
"""

"""
# 初回実行時は、Macにて下記の処理を実行して(ここでもブラウザが開く)、refresh_tokenを取得する
# SpotifyOAuthに渡す引数の値は、このファイルで同じ関数を実行している箇所と同一にする

```
oauth = SpotifyOAuth(client_id=client_id, ....)
secrets = oauth.get_access_token()
print(secrets['refresh_token'])
```

# このファイルと同じディレクトリ内にsecrets.jsonを作成して以下を書き込む
# {"refresh_token": <取得したrefresh_token>}

# それ以降は書き込んだrefresh_tokenを使ってaccess_tokenを取得することができる
"""

with open('./secrets.json', 'r') as f:
  secrets = json.load(f)
  refresh_token = secrets['refresh_token']

oauth = SpotifyOAuth(client_id=os.environ['SPOTIPY_CLIENT_ID'],
                     client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
                     redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'],
                     username=username,
                     scope=scope)
new_token = oauth.refresh_access_token(refresh_token)
sp = spotipy.Spotify(auth=new_token['access_token'])

with open('./secrets.json', 'w') as f:
  secrets['refresh_token'] = new_token['refresh_token']
  json.dump(secrets, f)

# https://github.com/plamere/spotipy/issues/211#issuecomment-369863112
# 古いVersionのSpotipyだとdevices()がundefinedになるため、上記の方法でUpgradeする
devices = sp.devices()
target_device_id = None
for dev in devices['devices']:
  if dev['name'].startswith('raspotify'):
    target_device_id = dev['id']
if target_device_id == None:
  raise Exception('target device not found')

def callback(ch):
  global PLAY_STATE
  if ch == NEXT:
    print('next track')
    sp.next_track(device_id=target_device_id)
  elif ch == START_STOP:
    if not PLAY_STATE:
      print('start track')
      sp.start_playback(device_id=target_device_id)
    else:
      print('pause track')
      sp.pause_playback(device_id=target_device_id)
    PLAY_STATE = not PLAY_STATE
  elif ch == PREV:
    print('prev track')
    sp.previous_track(device_id=target_device_id)

GPIO.setmode(GPIO.BCM)
GPIO.setup(NEXT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(START_STOP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(PREV, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(NEXT, GPIO.RISING, callback=callback, bouncetime=200)
GPIO.add_event_detect(START_STOP, GPIO.RISING, callback=callback, bouncetime=200)
GPIO.add_event_detect(PREV, GPIO.RISING, callback=callback, bouncetime=200)

try:
  print('start...')
  while True:
    sleep(0.01)

except KeyboardInterrupt:
  pass

GPIO.cleanup()

