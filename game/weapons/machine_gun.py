from ursina import Vec3, color
from game.weapons.base_weapon import BaseWeapon, Projectile
from game.config import GameConfig
import random


class MachineGun(BaseWeapon):
    # Visual properties for first-person view
    visual_model = "cube"
    visual_color = color.black
    visual_scale = (0.12, 0.18, 0.4)
    visual_position = (0.4, -0.3, 0.5)
    visual_rotation = (-10, 0, 0)
    
    # Audio
    sound_effect = 'machine_gun_fire'

    def __init__(self, owner=None):
        super().__init__(
            name="Machine Gun",
            damage=GameConfig.WEAPON_MACHINEGUN_DAMAGE,
            fire_rate=GameConfig.WEAPON_MACHINEGUN_FIRE_RATE,
            owner=owner,
        )

    def fire(self):
        if not self.owner:
            return

        spawn_position = self.owner.position + Vec3(0, 0.5, 0)

        direction = self.owner.forward

        accuracy_offset = Vec3(
            random.uniform(-0.05, 0.05),
            random.uniform(-0.05, 0.05),
            random.uniform(-0.05, 0.05),
        )
        direction = (direction + accuracy_offset).normalized()

        projectile = Projectile(
            position=spawn_position,
            direction=direction,
            speed=GameConfig.WEAPON_HANDGUN_PROJECTILE_SPEED * 1.2,
            damage=self.damage,
            lifetime=GameConfig.PROJECTILE_LIFETIME,
            size=GameConfig.WEAPON_HANDGUN_PROJECTILE_SIZE * 0.7,
            color=GameConfig.WEAPON_HANDGUN_PROJECTILE_COLOR,
            owner=self.owner,
        )

        self.projectiles.append(projectile)
