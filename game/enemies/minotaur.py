from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig


class Minotaur(BaseEnemy):
    def __init__(self, position, target):
        super().__init__(
            model="cube",
            position=position,
            target=target,
            health=GameConfig.ENEMY_MINOTAUR_HP,
            speed=GameConfig.ENEMY_MINOTAUR_SPEED,
            damage=GameConfig.ENEMY_MINOTAUR_DAMAGE,
            size=GameConfig.ENEMY_MINOTAUR_SIZE,
            color=GameConfig.ENEMY_MINOTAUR_COLOR,
            xp_value=GameConfig.XP_PER_MINOTAUR,
            score_value=GameConfig.SCORE_PER_KILL_MINOTAUR,
        )

    def ai_behavior(self):
        self.move_toward_target()

    def on_death(self):
        pass
