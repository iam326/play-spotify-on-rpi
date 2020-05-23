# play-spotify-on-rpi

## 環境

```
$ lsb_release -a
No LSB modules are available.
Distributor ID: Raspbian
Description:  Raspbian GNU/Linux 9.8 (stretch)
Release:  9.8
Codename: stretch

$ uname -a
Linux raspberrypi 4.9.59-v7+ #1047 SMP Sun Oct 29 12:19:23 GMT 2017 armv7l GNU/Linux

$ python3 --version
Python 3.5.3

$ pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.5)
```

## Setup

### raspotify の Setup

```
[参考]
http://hylom.net/spotify-with-raspberry-pi
https://ohmyenter.com/play-spotify-on-raspberry-pi/

// raspotify の install
$ curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

// raspotify の設定変更
$ sudo vim /etc/default/raspotify
...

# プレミアム会員だと設定可
BITRATE="320"

# イヤホンジャックから出力する
OPTIONS="--device hw:1,0"

# 音量の自動調整
VOLUME_ARGS="--enable-volume-normalisation --linear-volume --initial-volume=70"
...

$ sudo systemctl restart raspotify
```

### Spotify App の Setup

1. Spotify for Developers の Dashboard から CREATE AN APP する
1. EDIT SETTINGS から Redirect URIs に `http://127.0.0.1:8080/` を追加 & 保存する

### 音声関連

```
// マイクのカード番号とデバイス番号の確認 -> カード: 0, デバイス: 0
$ arecord -l
**** ハードウェアデバイス CAPTURE のリスト ****
カード 0: Device [USB PnP Audio Device], デバイス 0: USB Audio [USB Audio]
  サブデバイス: 1/1
  サブデバイス #0: subdevice #0

// 音声の録音
$ arecord -D plughw:0,0 test.wav

// スピーカーのカード番号とデバイス番号を確認 -> カード: 1, デバイス: 0
$ aplay -l
**** ハードウェアデバイス PLAYBACK のリスト ****
カード 1: ALSA [bcm2835 ALSA], デバイス 0: bcm2835 ALSA [bcm2835 ALSA]
サブデバイス: 7/7
サブデバイス #0: subdevice #0
サブデバイス #1: subdevice #1
サブデバイス #2: subdevice #2
サブデバイス #3: subdevice #3
サブデバイス #4: subdevice #4
サブデバイス #5: subdevice #5
サブデバイス #6: subdevice #6
...

// 音声の再生
$ aplay -D plughw:1,0 test.wav

// PyAudio の install (pip3 install は試していない)
$ sudo apt-get update
$ sudo apt-get install python3-pyaudio

// NumPy の install 
// $ ... 既に入っていたので別途確認が必要
```

