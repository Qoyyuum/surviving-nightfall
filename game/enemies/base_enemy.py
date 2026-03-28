from ursina import Entity, time, Vec3, destroy, distance, invoke
import math
import random

class BaseEnemy(Entity):
    # Class attributes for sound effects (override in subclasses)
    sound_spawn = None
    sound_attack = None
    sound_hurt = None
    sound_death = None
    
    def __init__(
        self,
        position,
        target,
        health,
        speed,
        damage,
        xp_value,
        score_value,
        size=1,
        color=None,
        **kwargs,
    ):
        # Only pass color if it's not None (for textured models)
        entity_kwargs = {"position": position, "scale": size, "collider": "box", **kwargs}
        if color is not None:
            entity_kwargs["color"] = color
        
        super().__init__(**entity_kwargs)

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
        self.audio_manager = None
        
        # Random growl timer (plays spawn sound randomly during lifetime)
        self.growl_timer = random.uniform(5.0, 15.0)
        self.next_growl_delay = random.uniform(10.0, 20.0)
        
        # Play spawn sound on creation
        self._play_spawn_sound()
        
    def take_damage(self, amount):
        if not self.is_alive:
            return False

        self.health -= amount
        
        # Play hurt sound
        self._play_hurt_sound()

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
        
        # Play death sound and delay destruction
        self._play_death_sound()
        invoke(lambda: destroy(self) if self else None, delay=0.5)

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
            
            # Play attack sound
            self._play_attack_sound()

    def update(self):
        if not self.is_alive:
            return

        # Check if game is paused
        if hasattr(self.target, 'game_manager') and self.target.game_manager.pause_menu.is_active:
            return

        if self.attack_cooldown > 0:
            self.attack_cooldown -= time.dt
        
        # Random growl timer
        if self.growl_timer > 0:
            self.growl_timer -= time.dt
            if self.growl_timer <= 0:
                self._play_spawn_sound()  # Reuse spawn sound as growl
                self.growl_timer = self.next_growl_delay
                self.next_growl_delay = random.uniform(10.0, 20.0)

        self.ai_behavior()
        self.check_collision_with_target()
    
    def _play_spawn_sound(self):
        """Play spawn/growl sound"""
        if self.sound_spawn and self.audio_manager:
            self.audio_manager.play_sfx(self.sound_spawn)
    
    def _play_attack_sound(self):
        """Play attack sound"""
        if self.sound_attack and self.audio_manager:
            self.audio_manager.play_sfx(self.sound_attack)
    
    def _play_hurt_sound(self):
        """Play hurt sound"""
        if self.sound_hurt and self.audio_manager:
            self.audio_manager.play_sfx(self.sound_hurt)
    
    def _play_death_sound(self):
        """Play death sound"""
        if self.sound_death and self.audio_manager:
            self.audio_manager.play_sfx(self.sound_death)

    def ai_behavior(self):
        pass
