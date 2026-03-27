from ursina import Entity, time, destroy, distance
from game.config import GameConfig
import math


class XPOrb(Entity):
    def __init__(self, position, xp_value, target):
        super().__init__(
            model="sphere",
            position=position,
            scale=GameConfig.XP_ORB_SIZE,
            color=GameConfig.XP_ORB_COLOR,
            collider="sphere",
        )

        self.xp_value = xp_value
        self.target = target
        self.magnetic_speed = 8.0
        self.magnetic_range = 5.0

    def update(self):
        if not self.target or not self.target.is_alive:
            return

        dist = distance(self.position, self.target.position)

        if dist < self.magnetic_range:
            direction = (self.target.position - self.position).normalized()
            self.position += direction * self.magnetic_speed * time.dt


class XPSystem:
    def __init__(self, player):
        self.player = player
        self.current_xp = 0
        self.current_level = 1
        self.xp_orbs = []
        self.pending_level_ups = 0

        self.on_level_up = None

    def get_xp_for_level(self, level):
        return int(
            GameConfig.XP_LEVEL_BASE
            * math.pow(GameConfig.XP_LEVEL_MULTIPLIER, level - 1)
        )

    def get_xp_required(self):
        return self.get_xp_for_level(self.current_level)

    def add_xp(self, amount):
        self.current_xp += amount

        while self.current_xp >= self.get_xp_required():
            self.current_xp -= self.get_xp_required()
            self.current_level += 1
            self.pending_level_ups += 1

            if self.on_level_up:
                self.on_level_up(self.current_level)

    def spawn_xp_orb(self, position, xp_value):
        orb = XPOrb(position, xp_value, self.player)
        self.xp_orbs.append(orb)

    def collect_orb(self, orb):
        if orb in self.xp_orbs:
            self.add_xp(orb.xp_value)
            self.xp_orbs.remove(orb)

    def get_xp_progress(self):
        required = self.get_xp_required()
        if required == 0:
            return 1.0
        return self.current_xp / required

    def reset(self):
        self.current_xp = 0
        self.current_level = 1
        self.pending_level_ups = 0

        for orb in self.xp_orbs:
            if orb:
                destroy(orb)
        self.xp_orbs.clear()

    def update(self):
        self.xp_orbs = [orb for orb in self.xp_orbs if orb and orb.enabled]
