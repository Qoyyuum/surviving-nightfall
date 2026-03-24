from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig
import random

class Ghost(BaseEnemy):
    def __init__(self, position, target):
        super().__init__(
            model='sphere',
            position=position,
            target=target,
            health=GameConfig.ENEMY_GHOST_HP,
            speed=GameConfig.ENEMY_GHOST_SPEED,
            damage=GameConfig.ENEMY_GHOST_DAMAGE,
            size=GameConfig.ENEMY_GHOST_SIZE,
            color=GameConfig.ENEMY_GHOST_COLOR,
            xp_value=GameConfig.XP_PER_GHOST,
            score_value=GameConfig.SCORE_PER_KILL_GHOST
        )
        
        self.dodge_chance = GameConfig.ENEMY_GHOST_DODGE_CHANCE
        
    def can_dodge(self):
        return random.random() < self.dodge_chance
        
    def ai_behavior(self):
        self.move_toward_target()
        
    def on_death(self):
        pass
