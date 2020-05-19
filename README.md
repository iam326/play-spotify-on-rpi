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
```

### Spotify App の Setup

1. Spotify for Developers の Dashboard から CREATE AN APP する
1. EDIT SETTINGS から Redirect URIs に `http://127.0.0.1:8080/` を追加 & 保存する

