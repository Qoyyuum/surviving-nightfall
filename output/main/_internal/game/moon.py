from ursina import Entity, color, time, PointLight
import math

# TODO: Fix moon visibility - moon is currently hidden by fog settings in wave_manager.update()
# Need to either:
# 1. Set moon.unlit=True and ensure it's not affected by fog
# 2. Move moon far enough away or adjust fog settings to not hide it
# 3. Use a different rendering approach for the moon (e.g., UI element or skybox)


class Moon(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model="sphere",
            scale=8,
            color=color.rgb32(220, 220, 180),
            unlit=False,
            **kwargs,
        )

        self.arc_radius = 60
        self.arc_height = 50
        self.movement_speed = 0.05
        self.time_offset = 0

        self.start_angle = math.pi * 0.8
        self.end_angle = math.pi * 0.2

        self.current_angle = self.start_angle

        self._update_position()
        # # Add dimlight around moon
        self.moon_light = PointLight(
            parent=self,
            color=color.rgb32(255, 220, 180),
            position=(0, 2, 0),
            attenuation=(0.1, 0.05, 0.02),
        )

    def _update_position(self):
        x = math.cos(self.current_angle) * self.arc_radius
        y = self.arc_height + math.sin(self.current_angle) * 20
        z = math.sin(self.current_angle) * self.arc_radius * 0.5

        self.position = (x, y, z)

    def update(self):
        self.current_angle -= self.movement_speed * time.dt

        if self.current_angle < self.end_angle:
            self.current_angle = self.start_angle

        self._update_position()
