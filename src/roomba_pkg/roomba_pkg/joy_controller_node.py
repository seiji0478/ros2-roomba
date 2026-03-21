import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from my_msgs.msg import RoombaController
from .config import JoyButtonsMap, JoyAxisMap


class JoyControllerNode(Node):
    def __init__(self):
        super().__init__('joy_controller')

        # Joy msg 用サブスクライバー
        self.sub = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10
            )

        # RoombaController msg 用パブリッシャー
        self.pub = self.create_publisher(
            RoombaController,
            '/roomba_controller',
            10
            )


        self.prev_bottons = []

    def joy_callback(self, msg):
        """
        Joy msg を RoombaController msg へ変換
        """
        # ルンバ用メッセージ初期化
        roomba_controller_msg = RoombaController()

        '''
        ボタン処理
        '''
        # 初回ボタン状態保存
        if not self.prev_bottons:
            self.prev_bottons = msg.buttons
            return

        for i, (prev, curr) in enumerate(zip(self.prev_bottons, msg.buttons)):
            # エッジ検出: 0 → 1
            if prev == 0 and curr == 1:
                if i == JoyButtonsMap.BTN_A.value:
                    """
                    Aボタン: ブラシON/OFF
                    """
                    roomba_controller_msg.brush_button = True
                elif i == JoyButtonsMap.BTN_B.value:
                    self.get_logger().info("Button B pressed")
                elif i == JoyButtonsMap.BTN_X.value:
                    self.get_logger().info("Button X pressed")
                elif i == JoyButtonsMap.BTN_Y.value:
                    self.get_logger().info("Button Y pressed")
                elif i == JoyButtonsMap.BTN_START.value:
                    """
                    STARTボタン: 電源ON/OFF
                    """
                    roomba_controller_msg.power_button = True
                elif i == JoyButtonsMap.BTN_BACK.value:
                    """
                    BACKボタン: Dock モード
                    """
                    roomba_controller_msg.dock_button = True
            # elif prev == 1 and curr == 0:
            #     self.get_logger().info(f"Button {JoyButtonsMap(i).name} released")

        # ボタン状態更新
        self.prev_bottons = msg.buttons

        '''
        軸処理
        '''
        for i, axis in enumerate(msg.axes):
            if i == JoyAxisMap.AXIS_DPAD_HORIZONTAL.value:
                roomba_controller_msg.dpad_angular = axis
            elif i == JoyAxisMap.AXIS_DPAD_VERTICAL.value:
                roomba_controller_msg.dpad_linear = axis
        # roomba_controller_msg.linear = msg.axes[1]
        # roomba_controller_msg.angular = msg.axes[0]

        # /roomba_controller トピックに publish
        self.pub.publish(roomba_controller_msg)

def main():
    rclpy.init()
    joy_controller_node = JoyControllerNode()
    rclpy.spin(joy_controller_node)
    rclpy.shutdown()