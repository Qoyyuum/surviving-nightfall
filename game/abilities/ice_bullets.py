from game.abilities.base_ability import BaseAbility
from game.config import GameConfig
from ursina import time

class IceBullets(BaseAbility):
    def __init__(self):
        super().__init__(
            name="Ice Bullets",
            description="Bullets slow enemies on hit"
        )
        
        self.slow_amount = GameConfig.ABILITY_ICE_BULLETS_SLOW
        self.slow_duration = GameConfig.ABILITY_ICE_BULLETS_DURATION
        
    def on_activate(self):
        pass
        
    def on_deactivate(self):
        pass
        
    def on_upgrade(self):
        self.slow_amount += 0.1
        self.slow_duration += 0.5
        
    def apply_slow(self, enemy):
        if not hasattr(enemy, 'ice_slow_timer'):
            enemy.ice_slow_timer = 0
            enemy.original_speed = enemy.speed
            
        enemy.ice_slow_timer = self.slow_duration
        enemy.speed = enemy.original_speed * self.slow_amount
        
    def update(self):
        pass
