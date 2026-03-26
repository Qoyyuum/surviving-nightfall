from game.abilities.base_ability import BaseAbility
from game.config import GameConfig
from ursina import time, distance, destroy, Entity, color
from ursina.models.procedural.cylinder import Cylinder
import random


class ArcLightning(BaseAbility):
    def __init__(self):
        super().__init__(
            name="Arc Lightning",
            description="Chain lightning damages nearby enemies",
            ui_model='cube',
            ui_color=(255, 255, 100)  # Yellow
        )

        self.damage = GameConfig.ABILITY_ARC_LIGHTNING_DAMAGE
        self.max_targets = GameConfig.ABILITY_ARC_LIGHTNING_TARGETS
        self.range = GameConfig.ABILITY_ARC_LIGHTNING_RANGE
        self.cooldown_time = GameConfig.ABILITY_ARC_LIGHTNING_COOLDOWN
        self.cooldown = 0

        self.lightning_effects = []

    def on_activate(self):
        pass

    def on_deactivate(self):
        for effect in self.lightning_effects:
            if effect:
                destroy(effect)
        self.lightning_effects.clear()

    def on_upgrade(self):
        self.damage += 10
        self.max_targets += 1

    def trigger(self, enemies):
        if self.cooldown > 0 or not self.owner:
            return []

        nearby_enemies = []
        for enemy in enemies:
            if enemy and enemy.is_alive:
                dist = distance(self.owner.position, enemy.position)
                if dist <= self.range:
                    nearby_enemies.append(enemy)

        if len(nearby_enemies) == 0:
            return []

        targets = random.sample(
            nearby_enemies, min(self.max_targets, len(nearby_enemies))
        )

        kills = []
        for target in targets:
            # Store enemy data before damaging (enemy might die)
            target_pos = target.position
            target_xp = target.xp_value
            target_score = target.score_value
            
            enemy_died = target.take_damage(self.damage)
            
            # Create lightning strike visual effect
            self._create_lightning_strike(target_pos)
            
            # Track kills for XP spawning
            if enemy_died:
                kills.append({
                    "enemy": target,
                    "xp": target_xp,
                    "score": target_score,
                    "position": target_pos
                })

        self.cooldown = self.cooldown_time
        return kills
    
    def _create_lightning_strike(self, target_position):
        """Create a lightning strike visual effect at target position"""
        # Create tall lightning bolt pillar that moves down
        bolt_height = 6
        bolt = Entity(
            model=Cylinder(resolution=8, radius=0.15, height=bolt_height),
            color=color.rgb32(255, 255, 150),  # Bright yellow
            scale=(1, 1, 1),
            position=(target_position.x, target_position.y + bolt_height/2 + 3, target_position.z),
            rotation=(0, 0, 0)
        )
        bolt.target_y = 0.1 + bolt_height/2  # Hit ground level, not enemy head
        bolt.start_y = bolt.y
        bolt.lifetime = 0.35  # Slower strike for better visibility
        bolt.age = 0
        bolt.is_bolt = True
        self.lightning_effects.append(bolt)
        
        # Create explosion particles at impact point
        num_particles = 12
        for i in range(num_particles):
            particle = Entity(
                model='sphere',
                color=color.rgb32(255, 255, 100),
                scale=0.06,
                position=(target_position.x, target_position.y + 0.2, target_position.z)
            )
            # Spread particles outward
            angle = (i / num_particles) * 3.14159 * 2
            particle.velocity_x = random.uniform(2, 4) * (1 if i % 2 == 0 else -1)
            particle.velocity_z = random.uniform(2, 4) * (1 if i % 3 == 0 else -1)
            particle.velocity_y = random.uniform(1, 3)
            particle.lifetime = 0.9  # Longer explosion duration
            particle.age = -0.35  # Delay until bolt hits
            particle.is_bolt = False
            self.lightning_effects.append(particle)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= time.dt
        
        # Update lightning effects
        for effect in self.lightning_effects[:]:
            if not effect:
                self.lightning_effects.remove(effect)
                continue
            
            effect.age += time.dt
            
            if hasattr(effect, 'is_bolt') and effect.is_bolt:
                # Lightning bolt moving down
                if effect.age < effect.lifetime:
                    progress = effect.age / effect.lifetime
                    # Move entire pillar downward
                    effect.y = effect.start_y - (effect.start_y - effect.target_y) * progress
                    effect.alpha = 0.9
                else:
                    # Bolt finished, remove it
                    destroy(effect)
                    self.lightning_effects.remove(effect)
            else:
                # Explosion particles
                if effect.age < 0:
                    # Not started yet (waiting for bolt)
                    continue
                
                # Move particles outward
                effect.x += effect.velocity_x * time.dt
                effect.z += effect.velocity_z * time.dt
                effect.y += effect.velocity_y * time.dt
                
                # Fade out and shrink
                progress = effect.age / effect.lifetime
                effect.alpha = (1 - progress) * 0.8
                effect.scale = 0.06 * (1 - progress * 0.7)
                
                # Remove old particles
                if effect.age >= effect.lifetime:
                    destroy(effect)
                    self.lightning_effects.remove(effect)
