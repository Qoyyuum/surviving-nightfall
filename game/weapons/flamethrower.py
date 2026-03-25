from ursina import Vec3, distance, time, mouse, color
from game.weapons.base_weapon import BaseWeapon, Projectile
from game.config import GameConfig
import random

class FlameProjectile(Projectile):
    def __init__(self, position, direction, speed, damage, lifetime, size, owner=None):
        super().__init__(
            position=position,
            direction=direction,
            speed=speed,
            damage=damage,
            lifetime=lifetime,
            size=size,
            color=color.rgb32(255, 100, 0),
            owner=owner
        )
        
        self.burn_damage = damage * 0.5
        self.burn_duration = 2.0


class Flamethrower(BaseWeapon):
    # Visual properties for first-person view
    visual_model = "cube"
    visual_color = color.red
    visual_scale = (0.15, 0.2, 0.5)
    visual_position = (0.4, -0.3, 0.5)
    visual_rotation = (-10, 0, 0)
    
    def __init__(self, owner=None):
        super().__init__(
            name="Flamethrower",
            damage=GameConfig.WEAPON_FLAMETHROWER_DAMAGE,
            fire_rate=GameConfig.WEAPON_FLAMETHROWER_FIRE_RATE,
            owner=owner
        )
        
        self.attack_range = GameConfig.WEAPON_FLAMETHROWER_RANGE
        
    def fire(self):
        if not self.owner:
            return
            
        spawn_position = self.owner.position + Vec3(0, 0.5, 0)
        
        base_direction = self.owner.forward
        
        spread = Vec3(
            random.uniform(-0.2, 0.2),
            random.uniform(-0.1, 0.1),
            random.uniform(-0.2, 0.2)
        )
        direction = (base_direction + spread).normalized()
        
        projectile = FlameProjectile(
            position=spawn_position,
            direction=direction,
            speed=GameConfig.WEAPON_HANDGUN_PROJECTILE_SPEED * 0.5,
            damage=self.damage,
            lifetime=self.attack_range / (GameConfig.WEAPON_HANDGUN_PROJECTILE_SPEED * 0.5),
            size=GameConfig.WEAPON_HANDGUN_PROJECTILE_SIZE * 1.5,
            owner=self.owner
        )
        
        self.projectiles.append(projectile)
