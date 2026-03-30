# ROS2 による Roomba 操作デモ
ROS2 を学習するにあたって、Roomba を操作する ROS2 パッケージを作成する。

## 1. システム構成
| コンポーネント | 型番 | 内容 |
| --- | --- | --- |
| Roomba 本体 | Roomba 880 | 操作対象 |
| シングルボードコンピュータ | Raspberry Pi 4 | Roomba 制御 |
| Webカメラ | Logitech C505 HD Webcam | Roomba 用カメラ |
| ノートパソコン | PC-LL750HS6W | 遠隔操作用 |
| ゲームパッド | Logitech F310 Gamepad | Roomba 用コントローラ |

## 2. 各種ドキュメント

[Roomba インターフェース仕様書](https://cdn-shop.adafruit.com/datasheets/create_2_Open_Interface_Spec.pdf)

## 3. ROS2 各種ノード

| パッケージ名 | ノード名 | 実行コンポーネント | 内容 |
| --- | --- | --- | --- |
| roomba_pkg | [joy_controller_node](src/roomba_pkg/roomba_pkg/joy_controller_node.py) | Raspberry Pi 4 | joy メッセージ変換ノード |
| roomba_pkg | [roomba_controller_node](src/roomba_pkg/roomba_pkg/roomba_controller_node.py) | Raspberry Pi 4 | Roomba 制御用のノード |
| usb_cam | usb_cam_node_exe | Raspberry Pi 4 | ゲームパッド用のノード |
| joy(or joy_linux) | joy_node(joy_linux_node) | PC-LL750HS6W | ゲームパッド用のノード |
| rqt_image-View | rqt_image_view | PC-LL750HS6W | カメラ映像表示 |


### Raspberry Pi 4 上のノードを起動
#### joy メッセージ変換ノード起動

```
$ ros2 run roomba_pkg joy_controller_node
```
#### Roomba 制御用ノード起動

```
$ ros2 run roomba_pkg roomba_controller_node
```

#### カメラノード起動

カメラの遅延等を防ぐために下記の設定でカメラを起動する。また、エンコードが yuv422_yuy2 なので、フォーマットを yuyv2rgb 指定する。

| 項目 | 値 |
| --- | --- |
| Format | yuyv2rgb |
| Width | 640px |
| Height | 480px |
| Framerate | 15 |

```
$ ros2 run usb_cam usb_cam_node_exe --ros-args -p pixel_format:=yuyv2rgb -p image_width:=640 -p image_height:=480 -p framerate:=15.0
```

### PC-LL750HS6W 上のノードを起動


#### joy ノード起動

```
$ ros2 run joy joy_node
```

#### rqt image view ノード起動

```
$ ros2 run rqt_image_view rqt_image_view
```


## 4. YOLO 用仮想環境
### yolo_env をアクティベート

※ライブラリが壊れることがあるらしいため、必ず ROS2 を読み込んだ後で、yolo_env をアクティベートする。

```
$ source ~/yolo_env/bin/activate
```

OpenCV と YOLO による物体検出プログラムを実行する。

```
$ cd ~/yolo_env
$ python roomba_viewer.py
```