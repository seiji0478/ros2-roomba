import time
import serial
import rclpy
from rclpy.node import Node
from my_msgs.msg import RoombaController
from .config import RoombaCommand, DeviceConfig

class RoombaControllerNode(Node):
    def __init__(self):
        super().__init__('roomba_controller')

        self.get_logger().info("Starting Roomba Controller Node")

        # 電源状態管理フラグ
        self.power_state = False
        self.brush_state = False

        self.ser = serial.Serial(DeviceConfig.SERIAL_PORT, DeviceConfig.BAUD_RATE)

        self.sub = self.create_subscription(
            RoombaController,
            '/roomba_controller',
            self.controller_callback,
            10
        )

    def controller_callback(self, msg):
        if msg.power_button:
            self.get_logger().info(f"power_button: {msg.power_button}")
            if not self.power_state:
                self.ser.write(bytes([RoombaCommand.START.value]))
                self.ser.write(bytes([RoombaCommand.SAFE.value]))
                self.power_state = True
                time.sleep(0.1)
                self.ser.write(bytes([RoombaCommand.LED.value, 0, 128, 255]))
                time.sleep(0.1)
                # 0番の曲、1音、ノート60（ド）、長さ32
                self.ser.write(bytes([RoombaCommand.SONG.value, 0, 1, 60, 32]))
                self.ser.write(bytes([RoombaCommand.PLAY.value, 0]))
                time.sleep(0.1)
                self.get_logger().info(f"Power ON: {self.power_state}")
            elif self.power_state:
                self.ser.write(bytes([
                    140, 0, 5,
                    76, 16,  # E
                    76, 16,  # E
                    0, 16,   # rest
                    76, 16,
                    72, 32   # C
                    ]))

                self.ser.write(bytes([141, 0]))
                time.sleep(0.1)
                self.ser.write(bytes([RoombaCommand.POWER_OFF.value]))
                self.power_state = False
                self.get_logger().info(f"Power OFF: {self.power_state}")
        elif msg.dock_button:
            self.get_logger().info(f"dock_button: {msg.dock_button}")
            self.ser.write(bytes([RoombaCommand.SEEK_DOCK.value]))

        if self.power_state:
            if msg.brush_button:
                if not self.brush_state:
                    """
                    main brush	-127〜127	メインブラシ
                    side brush	-127〜127	サイドブラシ
                    vacuum	0〜127	吸引
                    """
                    # self.ser.write(bytes([RoombaCommand.MOTORS.value, 127, 127, 127]))  # 全ブラシON
                    self.ser.write(bytes([RoombaCommand.MOTORS.value, 127, 0, 127]))
                    self.brush_state = True
                    self.get_logger().info("Brushes ON")
                else:
                    self.ser.write(bytes([RoombaCommand.MOTORS.value, 0, 0, 0]))  # 全ブラシOFF
                    self.brush_state = False
                    self.get_logger().info("Brushes OFF")
            linear = msg.dpad_linear
            angular = msg.dpad_angular
            self.get_logger().info(f"Received D-Pad: horizontal={linear}, vertical={angular}")
            if linear == 0 and angular == 0:
               cmd = [
                    RoombaCommand.DRIVE.value,
                    0, 0,  # velocity
                    0, 0   # radius
                ]
            else:
                speed_scale = 0.3
                # m/s → mm/s(ルンバ仕様)
                velocity = int(linear * 1000 * speed_scale)

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
                    RoombaCommand.DRIVE.value,
                    (velocity >> 8) & 0xFF,     # 8bit右シフト（上位8bit取得）
                    velocity & 0xFF,            # 下位8bit取得
                    (radius >> 8) & 0xFF,       # 8bit右シフト（上位8bit取得）
                    radius & 0xFF               # 下位8bit取得
                ]

            self.ser.write(bytes(cmd))

def main():
    rclpy.init()
    roomba_controller_node = RoombaControllerNode()
    rclpy.spin(roomba_controller_node)
    rclpy.shutdown()