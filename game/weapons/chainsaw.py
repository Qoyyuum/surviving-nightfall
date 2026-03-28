from ursina import distance, time, mouse, color
from game.weapons.base_weapon import BaseWeapon
from game.config import GameConfig


class Chainsaw(BaseWeapon):
    # Visual properties for first-person view
    visual_model = "cube"
    visual_color = color.orange
    visual_scale = (0.2, 0.2, 0.4)
    visual_position = (0.4, -0.3, 0.5)
    visual_rotation = (-10, 0, 0)
    
    # Audio
    sound_effect = 'chainsaw_fire'

    def __init__(self, owner=None):
        super().__init__(
            name="Chainsaw",
            damage=GameConfig.WEAPON_CHAINSAW_DAMAGE,
            fire_rate=GameConfig.WEAPON_CHAINSAW_FIRE_RATE,
            owner=owner,
        )

        self.attack_range = GameConfig.WEAPON_CHAINSAW_RANGE
        self.pushback_force = 2.0

    def update(self):
        if self.fire_cooldown > 0:
            self.fire_cooldown -= time.dt

        if mouse.left and self.owner and self.owner.is_alive:
            if self.fire_cooldown <= 0:
                self.fire()
                self.fire_cooldown = self.fire_rate

        self.projectiles = [p for p in self.projectiles if p and p.enabled]

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

                        if dot_product > 0.7:
                            enemy.take_damage(self.damage)

                            pushback_direction = (
                                enemy.position - self.owner.position
                            ).normalized()
                            enemy.position += (
                                pushback_direction * self.pushback_force * time.dt
                            )
