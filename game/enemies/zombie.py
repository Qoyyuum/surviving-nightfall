from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig

class Zombie(BaseEnemy):
    def __init__(self, position, target):
        super().__init__(
            model='cube',
            position=position,
            target=target,
            health=GameConfig.ENEMY_ZOMBIE_HP,
            speed=GameConfig.ENEMY_ZOMBIE_SPEED,
            damage=GameConfig.ENEMY_ZOMBIE_DAMAGE,
            size=GameConfig.ENEMY_ZOMBIE_SIZE,
            color=GameConfig.ENEMY_ZOMBIE_COLOR,
            xp_value=GameConfig.XP_PER_ZOMBIE,
            score_value=GameConfig.SCORE_PER_KILL_ZOMBIE
        )
        
    def ai_behavior(self):
        self.move_toward_target()
        
    def on_death(self):
        pass
