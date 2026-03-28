from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig
from ursina import time


class Cyclops(BaseEnemy):
    # Audio
    sound_spawn = 'cyclops_spawn'
    sound_attack = 'cyclops_attack'
    sound_hurt = 'cyclops_hurt'
    sound_death = 'cyclops_death'
    
    def __init__(self, position, target):
        super().__init__(
            model="assets/models/monsters/Cyclops.obj",
            position=position,
            target=target,
            health=GameConfig.ENEMY_CYCLOPS_HP,
            speed=GameConfig.ENEMY_CYCLOPS_SPEED,
            damage=GameConfig.ENEMY_CYCLOPS_DAMAGE,
            size=GameConfig.ENEMY_CYCLOPS_SIZE,
            xp_value=GameConfig.XP_PER_CYCLOPS,
            score_value=GameConfig.SCORE_PER_KILL_CYCLOPS,
        )

        self.burst_speed = GameConfig.ENEMY_CYCLOPS_SPEED_BURST
        self.burst_duration = GameConfig.ENEMY_CYCLOPS_BURST_DURATION
        self.burst_cooldown_time = GameConfig.ENEMY_CYCLOPS_BURST_COOLDOWN

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
