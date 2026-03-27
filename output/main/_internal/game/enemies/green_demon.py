from game.enemies.base_enemy import BaseEnemy
from game.config import GameConfig


class GreenDemon(BaseEnemy):
    def __init__(self, position, target):
        super().__init__(
            model="assets/models/monsters/GreenDemon.obj",
            position=position,
            target=target,
            health=GameConfig.ENEMY_GREEN_DEMON_HP,
            speed=GameConfig.ENEMY_GREEN_DEMON_SPEED,
            damage=GameConfig.ENEMY_GREEN_DEMON_DAMAGE,
            size=GameConfig.ENEMY_GREEN_DEMON_SIZE,
            xp_value=GameConfig.XP_PER_GREEN_DEMON,
            score_value=GameConfig.SCORE_PER_KILL_GREEN_DEMON,
        )

    def ai_behavior(self):
        self.move_toward_target()

    def on_death(self):
        pass
