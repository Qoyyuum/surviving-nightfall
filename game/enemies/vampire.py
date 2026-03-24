from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig
from ursina import time

class Vampire(BaseEnemy):
    def __init__(self, position, target):
        super().__init__(
            model='cube',
            position=position,
            target=target,
            health=GameConfig.ENEMY_VAMPIRE_HP,
            speed=GameConfig.ENEMY_VAMPIRE_SPEED,
            damage=GameConfig.ENEMY_VAMPIRE_DAMAGE,
            size=GameConfig.ENEMY_VAMPIRE_SIZE,
            color=GameConfig.ENEMY_VAMPIRE_COLOR,
            xp_value=GameConfig.XP_PER_VAMPIRE,
            score_value=GameConfig.SCORE_PER_KILL_VAMPIRE
        )
        
        self.burst_speed = GameConfig.ENEMY_VAMPIRE_SPEED_BURST
        self.burst_duration = GameConfig.ENEMY_VAMPIRE_BURST_DURATION
        self.burst_cooldown_time = GameConfig.ENEMY_VAMPIRE_BURST_COOLDOWN
        
        self.is_bursting = False
        self.burst_timer = 0
        self.burst_cooldown = 0
        
    def ai_behavior(self):
        if self.burst_cooldown > 0:
            self.burst_cooldown -= time.dt
            
        if self.is_bursting:
            self.burst_timer -= time.dt
            if self.burst_timer <= 0:
                self.is_bursting = False
                self.burst_cooldown = self.burst_cooldown_time
            self.move_toward_target(speed_multiplier=self.burst_speed / self.speed)
        else:
            if self.burst_cooldown <= 0:
                self.is_bursting = True
                self.burst_timer = self.burst_duration
            self.move_toward_target()
        
    def on_death(self):
        pass
