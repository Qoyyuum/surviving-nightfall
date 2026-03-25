from ursina import Vec3, Entity, color, destroy, distance, time
from game.weapons.base_weapon import BaseWeapon, Projectile
from game.config import GameConfig

class ExplosiveProjectile(Projectile):
    def __init__(self, position, direction, speed, damage, lifetime, size, color, explosion_radius, owner=None):
        super().__init__(position, direction, speed, damage, lifetime, size, color, owner)
        self.explosion_radius = explosion_radius
        self.has_exploded = False
        
    def explode(self, enemies):
        if self.has_exploded:
            return
            
        self.has_exploded = True
        
        for enemy in enemies:
            if enemy and enemy.is_alive:
                dist = distance(self.position, enemy.position)
                if dist <= self.explosion_radius:
                    enemy.take_damage(self.damage)
                    
                    knockback = (enemy.position - self.position).normalized()
                    enemy.position += knockback * 2.0
                    
        destroy(self)


class Bazooka(BaseWeapon):
    # Visual properties for first-person view
    visual_model = "cube"
    visual_color = color.olive
    visual_scale = (0.2, 0.25, 0.6)
    visual_position = (0.4, -0.3, 0.5)
    visual_rotation = (-10, 0, 0)
    
    def __init__(self, owner=None):
        super().__init__(
            name="Bazooka",
            damage=GameConfig.WEAPON_BAZOOKA_DAMAGE,
            fire_rate=GameConfig.WEAPON_BAZOOKA_FIRE_RATE,
            owner=owner
        )
        
        self.explosion_radius = GameConfig.WEAPON_BAZOOKA_EXPLOSION_RADIUS
        
    def fire(self):
        if not self.owner:
            return
            
        spawn_position = self.owner.position + Vec3(0, 0.5, 0)
        direction = self.owner.forward
        
        projectile = ExplosiveProjectile(
            position=spawn_position,
            direction=direction,
            speed=GameConfig.WEAPON_HANDGUN_PROJECTILE_SPEED * 0.6,
            damage=self.damage,
            lifetime=GameConfig.PROJECTILE_LIFETIME,
            size=GameConfig.WEAPON_HANDGUN_PROJECTILE_SIZE * 2,
            color=color.orange,
            explosion_radius=self.explosion_radius,
            owner=self.owner
        )
        
        self.projectiles.append(projectile)
