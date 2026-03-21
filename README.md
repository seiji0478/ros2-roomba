# ROS2 による Roomba 操作デモ
ROS2 を学習するにあたって、Roomba を操作する ROS2 パッケージを作成する。

## システム構成
| コンポーネント | 型番 | 内容 |
| --- | --- | --- |
| Roomba 本体 | Roomba 880 | 操作対象 |
| シングルボードコンピュータ | Raspberry Pi 4 | Roomba 制御 |
| Webカメラ | Logitech C505 HD Webcam | Roomba 用カメラ |
| ノートパソコン | PC-LL750HS6W | 遠隔操作用 |
| ゲームパッド | Logitech F310 Gamepad | Roomba 用コントローラ |

## 各種ドキュメント

[Roomba インターフェース仕様書](https://cdn-shop.adafruit.com/datasheets/create_2_Open_Interface_Spec.pdf)

## 各種ノード

| ノード名 | 実行コンポーネント | 内容 |
| --- | --- | --- |
| [roomba_controller_node](src/roomba_pkg/roomba_pkg/roomba_controller_node.py) | Raspberry Pi 4 | ルンバ制御用のノード |
| [joy_controller_node](src/roomba_pkg/roomba_pkg/joy_controller_node.py) | Raspberry Pi 4 | メッセージ変換ノード（joyノード用 -> roombaノード用） |
| joy_node | PC-LL750HS6W | ゲームパッド用のノード |





