from game.abilities.base_ability import BaseAbility
from game.config import GameConfig
from ursina import Entity, time, destroy, distance
import random


class FoodOrb(Entity):
    def __init__(self, position, heal_amount, target):
        super().__init__(
            model="sphere",
            position=position,
            scale=GameConfig.FOOD_ORB_SIZE,
            color=GameConfig.FOOD_ORB_COLOR,
            collider="sphere",
        )

        self.heal_amount = heal_amount
        self.target = target
        self.magnetic_speed = 6.0
        self.magnetic_range = 4.0

    def update(self):
        if not self.target or not self.target.is_alive:
            return

        dist = distance(self.position, self.target.position)

        if dist < self.magnetic_range:
            direction = (self.target.position - self.position).normalized()
            self.position += direction * self.magnetic_speed * time.dt


class Healing(BaseAbility):
    def __init__(self):
        super().__init__(
            name="Healing",
            description="Enemies drop food that heals you",
            ui_model='sphere',
            ui_color=(100, 255, 100)  # Green
        )

        self.heal_amount = GameConfig.ABILITY_HEALING_AMOUNT
        self.drop_chance = GameConfig.ABILITY_HEALING_DROP_CHANCE
        self.food_orbs = []

    def on_activate(self):
        pass

    def on_deactivate(self):
        for orb in self.food_orbs:
            if orb:
                destroy(orb)
        self.food_orbs.clear()

    def on_upgrade(self):
        self.heal_amount += 5
        self.drop_chance = min(0.5, self.drop_chance + 0.1)

    def try_spawn_food(self, position):
        if random.random() < self.drop_chance:
            orb = FoodOrb(position, self.heal_amount, self.owner)
            self.food_orbs.append(orb)

    def collect_food(self, orb):
        if orb in self.food_orbs and self.owner:
            self.owner.heal(orb.heal_amount)
            self.food_orbs.remove(orb)

    def update(self):
        self.food_orbs = [orb for orb in self.food_orbs if orb and orb.enabled]
