from ursina import Vec3
from game.weapons.base_weapon import BaseWeapon, Projectile
from game.config import GameConfig

class Handgun(BaseWeapon):
    def __init__(self, owner=None):
        super().__init__(
            name="Handgun",
            damage=GameConfig.WEAPON_HANDGUN_DAMAGE,
            fire_rate=GameConfig.WEAPON_HANDGUN_FIRE_RATE,
            owner=owner
        )
        
    def fire(self):
        if not self.owner:
            return
            
        spawn_position = self.owner.position + Vec3(0, 0.5, 0)
        
        direction = self.owner.forward
        
        projectile = Projectile(
            position=spawn_position,
            direction=direction,
            speed=GameConfig.WEAPON_HANDGUN_PROJECTILE_SPEED,
            damage=self.damage,
            lifetime=GameConfig.PROJECTILE_LIFETIME,
            size=GameConfig.WEAPON_HANDGUN_PROJECTILE_SIZE,
            color=GameConfig.WEAPON_HANDGUN_PROJECTILE_COLOR,
            owner=self.owner
        )
        
        self.projectiles.append(projectile)
