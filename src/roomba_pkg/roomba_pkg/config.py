from enum import Enum


class DeviceConfig:
    """
    デバイス設定定数
    """
    SERIAL_PORT = '/dev/ttyUSB0'    # シリアルポートのパス
    BAUD_RATE = 115200              # ボーレート
    TIMEOUT = 1                     # タイムアウト時間（秒）


class RoombaCommand(Enum):
    """
    Roomba コマンド定数
    """
    START = 128                     # 開始（必須）
    SAFE = 131                      # セーフモード
    FULL = 132                      # フルモード（完全制御）
    POWER_OFF = 133                 # 電源OFF
    SPOT = 134                      # スポットモード
    CLEAN = 135                     # クリーンモード
    MAX = 136                       # MAXモード
    DRIVE = 137                     # ドライブ（速度と半径を指定）
    MOTORS = 138                    # モーター制御
    LED = 139                       # LED制御
    SONG = 140                      # 曲定義
    PLAY = 141                      # 曲再生
    SENSORS = 142                   # センサー取得(パケットID指定)
    SEEK_DOCK = 143                 # ドックに向かう
    DRIVE_DIRECT = 145              # 直接ドライブ（左右の車輪速度を個別に指定）
    STREAM = 148                    # ストリーム開始
    STREAM_PAUSE = 150              # ストリーム一時停止


class RoombaMotor(Enum):
    """
    Roomba モーター定数
    """
    MAIN_BRUSH = 0                  # メインブラシ
    SIDE_BRUSH = 1                  # サイドブラシ
    VACUUM = 2                      # バキューム

class RoombaSensorPacketID(Enum):
    """
    Roomba センサーID定数
    """
    BUMPS_WALLS = 7                 # バンパーと壁センサー
    CLIFF_LEFT = 8                  # 左の段差センサー
    CLIFF_FRONT_LEFT = 9            # 前左の段差センサー
    CLIFF_FRONT_RIGHT = 10          # 前右の段差センサー
    CLIFF_RIGHT = 11                # 右の段差センサー
    VIRTUAL_WALL = 13               # バーチャルウォールセンサー
    OVERCURRENTS = 14               # 車輪落下センサー
    DIRT_DETECTED = 15              # ダート検出センサー
    BATT_STATUS = 21                # バッテリー残量
    BATT_VOLTAGE = 22               # バッテリー電圧
    BATT_CURRENT = 23               # バッテリー電流
    BATT_TEMPERATURE = 24           # バッテリー温度
    BATT_CHARGE = 25                # バッテリー残量
    BATT_CAPACITY = 26              # バッテリー容量


class JoyButtonsMap(Enum):
    """
    ゲームパッドボタンマッピング
    """
    BTN_A = 0
    BTN_B = 1
    BTN_X = 2
    BTN_Y = 3
    BTN_LEFT_BACK = 4
    BTN_RIGHT_BACK = 5
    BTN_BACK = 6
    BTN_START = 7
    BTN_LOGICOOL = 8
    BTN_STICK_LEFT = 9
    BTN_STICK_RIGHT = 10


class JoyAxisMap(Enum):
    """
    ゲームパッド軸マッピング
    """
    AXIS_LEFT_STICK_HORIZONTAL = 0
    AXIS_LEFT_STICK_VERTICAL = 1
    AXIS_LEFT_TRIGGER = 2
    AXIS_RIGHT_STICK_HORIZONTAL = 3
    AXIS_RIGHT_STICK_VERTICAL = 4
    AXIS_RIGHT_TRIGGER = 5
    AXIS_DPAD_HORIZONTAL = 6
    AXIS_DPAD_VERTICAL = 7