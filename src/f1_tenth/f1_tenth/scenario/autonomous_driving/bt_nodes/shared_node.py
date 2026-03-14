import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry

class ROS2NodeShared(Node):
    def __init__(self, node_name='bt_shared_node'):
        super().__init__(node_name)
        # BT 노드에서 사용하는 내부 플래그
        # 차량 제어 명령 publisher
        # odom 저장
        self.odom = None
        self.odom_received = False

        self.create_subscription(
            Odometry,
            '/vesc/odom',
            self._odom_cb,
            10
        )

        # 원본 controller와 같은 high_level 토픽 사용
        self.ackermann_pub = self.create_publisher(
            AckermannDriveStamped,
            '/vesc/high_level/ackermann_cmd',
            10
        )

    def _odom_cb(self, msg):
        self.odom = msg
        self.odom_received = True

    def publish_drive_command(self, speed: float, steering_angle: float):
        msg = AckermannDriveStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.drive.speed = speed
        msg.drive.steering_angle = steering_angle

        self.ackermann_pub.publish(msg)

        self.get_logger().info(
            f'[Shared] publish speed={speed:.2f}, steering={steering_angle:.2f}'
        )

    def stop_vehicle(self):
        # 정지 명령도 같은 형식으로 publish
        self.publish_drive_command(0.0, 0.0)