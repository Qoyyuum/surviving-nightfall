from ursina import Entity, time, Vec3, destroy, distance
import math

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
        self.all_enemies = []
        
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
        
    def separate_from_enemies(self):
        """Push away from nearby enemies to prevent overlap"""
        separation_force = Vec3(0, 0, 0)
        separation_radius = 2.5
        
        for other in self.all_enemies:
            if other is self or not other.is_alive:
                continue
            
            diff = self.position - other.position
            diff.y = 0
            dist = diff.length()
            
            if dist < separation_radius and dist > 0.01:
                push_direction = diff.normalized()
                push_strength = ((separation_radius - dist) / separation_radius) * 2.0
                separation_force += push_direction * push_strength
        
        return separation_force
    
    def move_toward_target(self, speed_multiplier=1.0):
        if not self.target or not self.target.is_alive:
            return
        
        target_dir = self.target.position - self.position
        target_dir.y = 0
        
        if target_dir.length() < 0.01:
            return
        
        direction = target_dir.normalized()
        separation = self.separate_from_enemies()
        
        combined = direction + separation
        
        if combined.length() < 0.01:
            final_direction = direction
        else:
            final_direction = combined.normalized()
        
        movement = final_direction * self.speed * speed_multiplier * time.dt
        movement.y = 0
        
        self.position += movement
        self.y = 1
        
        angle = math.degrees(math.atan2(target_dir.x, target_dir.z))
        self.rotation_y = angle
        
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
