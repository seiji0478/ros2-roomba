import cv2
import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from ultralytics import YOLO


class ImageViewerNode(Node):

    def __init__(self):
        super().__init__('image_viewer')                    # ノード名を設定して初期化
        self.model = YOLO("yolov8n.pt")                     # YOLOモデル
        self.subscription = self.create_subscription(
            CompressedImage,                                # メッセージ型（圧縮画像）
            '/image_raw/compressed',                        # トピック名
            self.listener_callback,                         # コールバック関数
            10                                              # キューサイズ
        )

    def listener_callback(self, msg):
        """
        JPEGデータ(バイト列)を OpenCV でデコードし画面を表示
        """
        try:
            np_arr = np.frombuffer(msg.data, np.uint8)      # バイト列を配列変換
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)  # JPEGデータをOpenCV画像(BGR)変換

            if frame is None:
                return

            results = self.model(frame)                     # YOLO物体検出
            annotated_frame = results[0].plot()             # 描画
            cv2.imshow('Roomba Camera', annotated_frame)    # 画像表示
            cv2.waitKey(1)                                  # 1[ms]待機してウィンドウ更新
        except Exception as e:
            self.get_logger().error(f"Error: {e}")

def main(args=None):
    rclpy.init(args=args)       # ROS2クライアントライブラリ初期化
    node = ImageViewerNode()    # ImageViewerNodeインスタンス生成
    rclpy.spin(node)            # ノードが終了するまで待機
    node.destroy_node()         # ノードの破棄
    rclpy.shutdown()            # ROS2クライアントライブラリシャットダウン
    cv2.destroyAllwindows()     # OpenCVのウィンドウを閉じる

if __name__ == '__main__':
    main()