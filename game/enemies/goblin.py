from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig
from ursina import time, Vec3
import random

class Goblin(BaseEnemy):
    def __init__(self, position, target):
        super().__init__(
            model='cube',
            position=position,
            target=target,
            health=GameConfig.ENEMY_GOBLIN_HP,
            speed=GameConfig.ENEMY_GOBLIN_SPEED,
            damage=GameConfig.ENEMY_GOBLIN_DAMAGE,
            size=GameConfig.ENEMY_GOBLIN_SIZE,
            color=GameConfig.ENEMY_GOBLIN_COLOR,
            xp_value=GameConfig.XP_PER_GOBLIN,
            score_value=GameConfig.SCORE_PER_KILL_GOBLIN
        )
        
        self.jump_cooldown_time = GameConfig.ENEMY_GOBLIN_JUMP_COOLDOWN
        self.jump_distance = GameConfig.ENEMY_GOBLIN_JUMP_DISTANCE
        self.jump_cooldown = random.uniform(2, 4)
        
        self.is_jumping = False
        self.jump_timer = 0
        self.jump_duration = 0.5
        self.jump_start_pos = None
        self.jump_target_pos = None
        
    def ai_behavior(self):
        if self.jump_cooldown > 0:
            self.jump_cooldown -= time.dt
            
        if self.is_jumping:
            self.jump_timer += time.dt
            progress = min(self.jump_timer / self.jump_duration, 1.0)
            
            self.position = self.jump_start_pos + (self.jump_target_pos - self.jump_start_pos) * progress
            
            jump_height = 2.0 * (1 - abs(progress * 2 - 1))
            self.y = self.jump_start_pos.y + jump_height
            
            if progress >= 1.0:
                self.is_jumping = False
                self.jump_cooldown = self.jump_cooldown_time
        else:
            if self.jump_cooldown <= 0 and self.target and self.target.is_alive:
                direction = (self.target.position - self.position).normalized()
                self.jump_start_pos = self.position.copy()
                self.jump_target_pos = self.position + direction * self.jump_distance
                self.jump_target_pos.y = self.jump_start_pos.y
                
                self.is_jumping = True
                self.jump_timer = 0
            else:
                self.move_toward_target()
        
    def on_death(self):
        pass
