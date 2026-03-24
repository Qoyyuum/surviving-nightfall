from ursina import Entity, time, Vec3, destroy, mouse

class Projectile(Entity):
    def __init__(self, position, direction, speed, damage, lifetime, size, color, owner=None, **kwargs):
        super().__init__(
            model='sphere',
            position=position,
            scale=size,
            color=color,
            collider='sphere',
            **kwargs
        )
        
        self.direction = direction.normalized()
        self.speed = speed
        self.damage = damage
        self.lifetime = lifetime
        self.owner = owner
        self.age = 0
        
    def update(self):
        self.age += time.dt
        
        if self.age >= self.lifetime:
            destroy(self)
            return
            
        self.position += self.direction * self.speed * time.dt


class BaseWeapon:
    def __init__(self, name, damage, fire_rate, owner=None):
        self.name = name
        self.damage = damage
        self.fire_rate = fire_rate
        self.owner = owner
        self.fire_cooldown = 0
        self.projectiles = []
        
    def can_fire(self):
        return self.fire_cooldown <= 0
        
    def try_fire(self):
        if self.can_fire() and self.owner and self.owner.is_alive:
            self.fire()
            self.fire_cooldown = self.fire_rate
            
    def fire(self):
        pass
        
    def update(self):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= time.dt
            
        if mouse.left and self.owner and self.owner.is_alive:
            self.try_fire()
            
        self.projectiles = [p for p in self.projectiles if p and p.enabled]
        
    def cleanup(self):
        for projectile in self.projectiles:
            if projectile:
                destroy(projectile)
        self.projectiles.clear()
