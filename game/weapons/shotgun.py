from ursina import Vec3
from game.weapons.base_weapon import BaseWeapon, Projectile
from game.config import GameConfig
import math

class Shotgun(BaseWeapon):
    def __init__(self, owner=None):
        super().__init__(
            name="Shotgun",
            damage=GameConfig.WEAPON_SHOTGUN_DAMAGE,
            fire_rate=GameConfig.WEAPON_SHOTGUN_FIRE_RATE,
            owner=owner
        )
        
        self.pellet_count = GameConfig.WEAPON_SHOTGUN_PELLETS
        self.spread_angle = GameConfig.WEAPON_SHOTGUN_SPREAD
        
    def fire(self):
        if not self.owner:
            return
            
        spawn_position = self.owner.position + Vec3(0, 0.5, 0)
        base_direction = self.owner.forward
        
        for i in range(self.pellet_count):
            angle_offset = (i - self.pellet_count / 2) * (self.spread_angle / self.pellet_count)
            angle_rad = math.radians(angle_offset)
            
            rotated_direction = Vec3(
                base_direction.x * math.cos(angle_rad) - base_direction.z * math.sin(angle_rad),
                base_direction.y,
                base_direction.x * math.sin(angle_rad) + base_direction.z * math.cos(angle_rad)
            ).normalized()
            
            projectile = Projectile(
                position=spawn_position,
                direction=rotated_direction,
                speed=GameConfig.WEAPON_HANDGUN_PROJECTILE_SPEED,
                damage=self.damage,
                lifetime=GameConfig.PROJECTILE_LIFETIME,
                size=GameConfig.WEAPON_HANDGUN_PROJECTILE_SIZE * 0.8,
                color=GameConfig.WEAPON_HANDGUN_PROJECTILE_COLOR,
                owner=self.owner
            )
            
            self.projectiles.append(projectile)
