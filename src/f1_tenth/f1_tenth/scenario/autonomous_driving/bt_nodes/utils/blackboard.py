from enum import Enum, auto


class VehicleMode(Enum):
    MC = auto()
    FW = auto()


class FireBlackboard:
    def __init__(self):
        # --- Vehicle mode ---
        self.vehicle_mode: VehicleMode = VehicleMode.MC
        self.requested_mode: VehicleMode | None = None

        # --- Patrol ---
        self.patrol_index: int = 0
        self.num_patrol_points: int = 0

        # --- Position ---
        self.current_position = None
        self.target_position = None
        self.arrived_threshold: float = 1.0

        # --- Fire ---
        self.fire_detected: bool = False
        self.fire_handled: bool = False

        # --- Transition readiness ---
        self.ready_for_fw: bool = False
        self.ready_for_mc: bool = False
