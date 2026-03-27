from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig


class Cthulhu(BaseEnemy):
    def __init__(self, position, target):
        super().__init__(
            model="assets/models/monsters/Cthulhu.obj",
            position=position,
            target=target,
            health=GameConfig.ENEMY_CTHULHU_HP,
            speed=GameConfig.ENEMY_CTHULHU_SPEED,
            damage=GameConfig.ENEMY_CTHULHU_DAMAGE,
            size=GameConfig.ENEMY_CTHULHU_SIZE,
            xp_value=GameConfig.XP_PER_CTHULHU,
            score_value=GameConfig.SCORE_PER_KILL_CTHULHU,
        )

    def ai_behavior(self):
        self.move_toward_target()

    def on_death(self):
        pass
