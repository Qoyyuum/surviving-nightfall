from ursina import camera, lerp, Vec3, mouse
from game.config import GameConfig


class ThirdPersonCamera:
    def __init__(self, target):
        self.target = target
        self.offset = GameConfig.CAMERA_OFFSET
        self.smoothing = GameConfig.CAMERA_SMOOTHING

        camera.rotation_x = GameConfig.CAMERA_ROTATION.x
        camera.rotation_y = GameConfig.CAMERA_ROTATION.y
        camera.rotation_z = GameConfig.CAMERA_ROTATION.z

        self.mouse_sensitivity = 0.2

    def update(self):
        if not self.target or not self.target.is_alive:
            return

        target_rotation = self.target.rotation_y + mouse.x * self.mouse_sensitivity
        self.target.rotation_y = target_rotation

        rotated_offset = Vec3(self.offset.x, self.offset.y, self.offset.z)

        import math

        angle_rad = math.radians(self.target.rotation_y)
        rotated_x = rotated_offset.x * math.cos(
            angle_rad
        ) - rotated_offset.z * math.sin(angle_rad)
        rotated_z = rotated_offset.x * math.sin(
            angle_rad
        ) + rotated_offset.z * math.cos(angle_rad)

        desired_position = self.target.position + Vec3(
            rotated_x, rotated_offset.y, rotated_z
        )

        camera.position = Vec3(
            lerp(camera.position.x, desired_position.x, self.smoothing),
            lerp(camera.position.y, desired_position.y, self.smoothing),
            lerp(camera.position.z, desired_position.z, self.smoothing),
        )

        camera.look_at(self.target.position + Vec3(0, 1, 0))
