import serial
import rclpy                            # ROS2 ライブラリ
from rclpy.node import Node             # ノードの基本クラス
from geometry_msgs.msg import Twist     # 速度指令メッセージ
from .config import RoombaCommand


class RoombaNode(Node):
    def __init__(self):
        super().__init__('roomba_node')

        try:
            self.ser = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)
        except Exception as e:
            self.get_logger().error(f"Serial error: {e}")
            return

        self.start_roomba()

        """
        Subscriber を生成し、cmd_vel トピックから Twist メッセージを受け取る
            - cmd_vel トピックは、ロボットの速度指令を表す標準的なトピック
            - Twist メッセージタイプ
                linear.x    : 線形速度（前後速度）
                angular.z   : 角速度（回転速度）
        """
        self.subscription = self.create_subscription(
            Twist,                  # メッセージタイプ
            'cmd_vel',              # トピック名
            self.cmd_vel_callback,  # コールバック関数
            10                      # QoS(キューサイズ)
        )

    def start_roomba(self):
        self.ser.write(bytes([RoombaCommand.START]))    # Roomba 起動
        self.ser.write(bytes([RoombaCommand.SAFE]))     # セーフモード切替え

    def cmd_vel_callback(self, msg):
        """
        cmd_vel トピックからの Twist メッセージ処理し、Roomba に速度指令を送る
        """
        # Twist メッセージから線形速度と角速度を取得
        linear = msg.linear.x
        angular = msg.angular.z

        # m/s → mm/s(ルンバ仕様)
        velocity = int(linear * 1000)

        if angular == 0:
            # 半径: 0x8000 → 直進
            radius = 0x8000
        elif linear == 0:
            # radius: 1 → 左回転、-1 → 右回転
            velocity = int(abs(angular) * 200)
            radius = 1 if angular > 0 else -1
        else:
            # 曲線移動
            radius = int(linear / angular)

        """
        cmd 配列の構成:
        - 137: Drive コマンド
        - velocity_high, velocity_low: 速度の上位バイトと下位バイト
        - radius_high, radius_low: 半径の上位バイトと下位バイト
        ※16[bit]値を2バイトに分割して構成
        """
        cmd = [
            RoombaCommand.DRIVE,
            (velocity >> 8) & 0xFF,
            velocity & 0xFF,
            (radius >> 8) & 0xFF,
            radius & 0xFF
        ]

        self.ser.write(bytes(cmd))

def main(args=None):
    rclpy.init(args=args)   # ROS2 ノード初期化
    node = RoombaNode()     # RoombaNode インスタンス生成
    rclpy.spin(node)        # ノードが終了するまでスピン（待機）
    node.destroy_node()     # ノードクリーンアップ
    rclpy.shutdown()        # ROS2 シャットダウン