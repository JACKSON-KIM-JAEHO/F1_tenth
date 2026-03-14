import rclpy
from rclpy.executors import MultiThreadedExecutor
import threading
import os
import time
from ament_index_python.packages import get_package_share_directory

from .bt_nodes.shared_node import ROS2NodeShared
from f1_tenth.modules.bt_constructor import build_behavior_tree
from f1_tenth.modules.base_bt_nodes import Status


def main(args=None):
    rclpy.init(args=args)

    # 1. Shared ROS2 Node 생성
    shared = ROS2NodeShared(node_name='bt_runner_node')

    # 2. Executor 실행
    executor = MultiThreadedExecutor()
    executor.add_node(shared)
    spin_thread = threading.Thread(target=executor.spin, daemon=True)
    spin_thread.start()

    shared.get_logger().info("[MAIN] Shared node started")

    # 3. BT XML 경로
    pkg_share = get_package_share_directory("f1_tenth")
    xml_path = os.path.join(
        pkg_share,
        "scenario",
        "autonomous_driving",
        "main_bt.xml"
    )

    shared.get_logger().info(f"[MAIN] Loading BT XML: {xml_path}")

    # 4. BT 생성
    root = build_behavior_tree(shared, xml_path)
    shared.get_logger().info("[MAIN] Behavior Tree started")

    # 5. Tick loop
    try:
        while rclpy.ok():
            status = root.tick()

            if status == Status.SUCCESS:
                shared.get_logger().info("[BT] Mission completed")
                break

            if status == Status.FAILURE:
                shared.get_logger().warn("[BT] Mission failed")
                break

            time.sleep(0.05)

    except KeyboardInterrupt:
        shared.get_logger().warn("[MAIN] KeyboardInterrupt")

    finally:
        executor.shutdown()
        shared.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()