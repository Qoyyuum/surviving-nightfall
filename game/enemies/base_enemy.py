from ursina import Entity, time, Vec3, destroy, distance

class BaseEnemy(Entity):
    def __init__(self, position, target, health, speed, damage, size, color, xp_value, score_value, **kwargs):
        super().__init__(
            position=position,
            scale=size,
            color=color,
            collider='box',
            **kwargs
        )
        
        self.target = target
        self.max_health = health
        self.health = health
        self.speed = speed
        self.damage = damage
        self.xp_value = xp_value
        self.score_value = score_value
        
        self.is_alive = True
        self.attack_cooldown = 0
        self.attack_cooldown_time = 1.0
        
    def take_damage(self, amount):
        if not self.is_alive:
            return False
            
        self.health -= amount
        
        if self.health <= 0:
            self.health = 0
            self.die()
            return True
        return False
    
    def destroy(self):
        "Force destroy the enemy, even if it's already dead"
        if self.is_alive:
            self.die()
        
    def die(self):
        self.is_alive = False
        self.on_death()
        destroy(self)
        
    def on_death(self):
        pass
        
    def move_toward_target(self, speed_multiplier=1.0):
        if not self.target or not self.target.is_alive:
            return
            
        direction = (self.target.position - self.position).normalized()
        self.position += direction * self.speed * speed_multiplier * time.dt
        
        self.look_at(self.target.position)
        
    def check_collision_with_target(self):
        if not self.target or not self.target.is_alive or not self.is_alive:
            return
            
        dist = distance(self.position, self.target.position)
        
        if dist < 1.5 and self.attack_cooldown <= 0:
            self.target.take_damage(self.damage)
            self.attack_cooldown = self.attack_cooldown_time
            
    def update(self):
        if not self.is_alive:
            return
            
        if self.attack_cooldown > 0:
            self.attack_cooldown -= time.dt
            
        self.ai_behavior()
        self.check_collision_with_target()
        
    def ai_behavior(self):
        pass
