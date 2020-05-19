# play-spotify-on-rpi

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

