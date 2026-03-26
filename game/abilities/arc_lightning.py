from game.abilities.base_ability import BaseAbility
from game.config import GameConfig
from ursina import time, distance, destroy
import random


class ArcLightning(BaseAbility):
    def __init__(self):
        super().__init__(
            name="Arc Lightning", description="Chain lightning damages nearby enemies"
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
            return

        nearby_enemies = []
        for enemy in enemies:
            if enemy and enemy.is_alive:
                dist = distance(self.owner.position, enemy.position)
                if dist <= self.range:
                    nearby_enemies.append(enemy)

        if len(nearby_enemies) == 0:
            return

        targets = random.sample(
            nearby_enemies, min(self.max_targets, len(nearby_enemies))
        )

        for target in targets:
            target.take_damage(self.damage)

        self.cooldown = self.cooldown_time

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= time.dt
