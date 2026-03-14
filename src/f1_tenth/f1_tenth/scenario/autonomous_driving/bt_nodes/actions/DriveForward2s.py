from f1_tenth.modules.base_bt_nodes import BTNode, Status


class DriveForward2s(BTNode):

    def __init__(self, name, shared):
        super().__init__(name)

        self.shared = shared

        # driving parameters
        self.duration = 3.0
        self.speed = 2.0
        self.steering_angle = 0.0

        self.start_time = None
        self.done = False

    def tick(self):

        # 이미 완료된 경우
        if self.done:
            return Status.SUCCESS

        now = self.shared.get_clock().now().nanoseconds * 1e-9

        # 시작 시점 기록
        if self.start_time is None:
            self.start_time = now
            self.shared.get_logger().info('[BT][DriveForward] START')

        elapsed = now - self.start_time

        # 주행 중
        if elapsed < self.duration:

            self.shared.publish_drive_command(
                speed=self.speed,
                steering_angle=self.steering_angle
            )

            self.shared.get_logger().info(
                f'[BT][DriveForward] running... {elapsed:.2f}s'
            )

            return Status.RUNNING

        # 종료 → 차량 정지
        self.shared.stop_vehicle()

        self.shared.get_logger().info('[BT][DriveForward] SUCCESS')

        self.done = True
        return Status.SUCCESS

    def reset(self):
        """
        BT가 다시 실행될 때 상태 초기화
        """
        self.start_time = None
        self.done = False