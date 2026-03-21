import Enum

class RoombaCommand(Enum):
    START = 128         # 開始（必須）
    SAFE = 131          # セーフモード
    FULL = 132          # フルモード（完全制御）
    POWER = 133         # 電源OFF
    SPOT = 134          # スポットモード
    CLEAN = 135         # クリーンモード
    MAX = 136           # MAXモード
    DRIVE = 137         # ドライブ（速度と半径を指定）
    DRIVE_DIRECT = 145  # 直接ドライブ（左右の車輪速度を個別に指定）
    MOTORS = 138        # モーター制御
    LEDS = 139          # LED制御
    SONG = 140          # 曲定義
    PLAY = 141          # 曲再生
    SENSORS = 142       # センサー取得
    STREAM = 148        # ストリーム開始
    STREAM_PAUSE = 150  # ストリーム一時停止