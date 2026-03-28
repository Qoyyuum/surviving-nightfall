from ursina import distance, color
from game.weapons.base_weapon import BaseWeapon
from game.config import GameConfig


class Katana(BaseWeapon):
    # Visual properties for first-person view
    visual_model = "cube"
    visual_color = color.cyan
    visual_scale = (0.05, 0.05, 0.8)
    visual_position = (0.4, -0.3, 0.5)
    visual_rotation = (-10, 0, 0)
    
    # Audio
    sound_effect = 'katana_swing'

    def __init__(self, owner=None):
        super().__init__(
            name="Katana",
            damage=GameConfig.WEAPON_KATANA_DAMAGE,
            fire_rate=GameConfig.WEAPON_KATANA_FIRE_RATE,
            owner=owner,
        )

        self.attack_range = GameConfig.WEAPON_KATANA_RANGE
        self.bleed_damage = 5
        self.bleed_duration = 3.0

    def fire(self):
        if not self.owner:
            return

        if hasattr(self.owner, "game_manager") and hasattr(
            self.owner.game_manager, "wave_manager"
        ):
            wave_manager = self.owner.game_manager.wave_manager

            for enemy in wave_manager.enemies:
                if enemy and enemy.is_alive:
                    dist = distance(self.owner.position, enemy.position)

                    if dist <= self.attack_range:
                        forward_to_enemy = (
                            enemy.position - self.owner.position
                        ).normalized()
                        dot_product = self.owner.forward.dot(forward_to_enemy)

                        if dot_product > 0.5:
                            enemy.take_damage(self.damage)

                            if not hasattr(enemy, "bleed_timer"):
                                enemy.bleed_timer = 0
                                enemy.bleed_damage = self.bleed_damage

                            enemy.bleed_timer = self.bleed_duration
