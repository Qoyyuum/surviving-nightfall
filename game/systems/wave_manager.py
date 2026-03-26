from ursina import time, Vec3, scene, color, window
import random
import math
from game.config import GameConfig
from game.enemies.zombie import Zombie
from game.enemies.ghost import Ghost
from game.enemies.vampire import Vampire
from game.enemies.goblin import Goblin
from game.enemies.minotaur import Minotaur


class WaveManager:
    def __init__(self, player):
        self.player = player
        self.current_wave = 0
        self.max_waves = 5
        self.enemies = []
        self.wave_active = False
        self.spawn_timer = 0
        self.spawn_queue = []

        self.wave_configs = {
            1: GameConfig.WAVE_1_ENEMIES,
            2: GameConfig.WAVE_2_ENEMIES,
            3: GameConfig.WAVE_3_ENEMIES,
            4: GameConfig.WAVE_4_ENEMIES,
            5: GameConfig.WAVE_5_ENEMIES,
        }

        self.on_wave_complete = None
        self.on_all_waves_complete = None

    def set_fog(self):
        scene.fog_color = color.black
        scene.fog_density = (0, 15)
        window.color = scene.fog_color

    def start_wave(self, wave_number):
        if wave_number < 1 or wave_number > self.max_waves:
            return

        self.current_wave = wave_number
        self.wave_active = True
        self.spawn_queue = []

        wave_config = self.wave_configs[wave_number]

        for enemy_type, count in wave_config.items():
            for _ in range(count):
                self.spawn_queue.append(enemy_type)

        random.shuffle(self.spawn_queue)
        self.spawn_timer = 0

        print(f"=== WAVE {wave_number} STARTED ===")
        print(f"Enemies to spawn: {len(self.spawn_queue)}")
        print(f"Spawn queue: {self.spawn_queue}")

    def spawn_enemy(self, enemy_type):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(
            GameConfig.SPAWN_RADIUS_MIN, GameConfig.SPAWN_RADIUS_MAX
        )

        spawn_x = self.player.x + math.cos(angle) * distance
        spawn_z = self.player.z + math.sin(angle) * distance

        boundary = GameConfig.GROUND_SIZE / 2 - 2
        spawn_x = max(-boundary, min(boundary, spawn_x))
        spawn_z = max(-boundary, min(boundary, spawn_z))

        spawn_pos = Vec3(spawn_x, 1, spawn_z)

        enemy = None
        if enemy_type == "zombie":
            enemy = Zombie(spawn_pos, self.player)
        elif enemy_type == "ghost":
            enemy = Ghost(spawn_pos, self.player)
        elif enemy_type == "vampire":
            enemy = Vampire(spawn_pos, self.player)
        elif enemy_type == "goblin":
            enemy = Goblin(spawn_pos, self.player)
        elif enemy_type == "minotaur":
            enemy = Minotaur(spawn_pos, self.player)

        if enemy:
            enemy.all_enemies = self.enemies
            self.enemies.append(enemy)
            print(
                f"Spawned {enemy_type} at ({spawn_x:.1f}, {spawn_z:.1f}) - Total enemies: {len(self.enemies)}"
            )

    def is_wave_complete(self):
        return len(self.spawn_queue) == 0 and len(self.enemies) == 0

    def update(self):
        self.set_fog()
        if not self.wave_active:
            return

        # Update all enemies
        for enemy in self.enemies:
            if enemy and enemy.is_alive:
                enemy.update()

        # Clean up dead enemies
        alive_before = len(self.enemies)
        self.enemies = [e for e in self.enemies if e and e.is_alive]
        if alive_before != len(self.enemies):
            print(f"Enemies alive: {len(self.enemies)}")

        if len(self.spawn_queue) > 0:
            self.spawn_timer += time.dt

            if self.spawn_timer >= GameConfig.SPAWN_STAGGER_TIME:
                enemy_type = self.spawn_queue.pop(0)
                self.spawn_enemy(enemy_type)
                self.spawn_timer = 0

        if self.is_wave_complete():
            self.wave_active = False

            if self.current_wave >= self.max_waves:
                if self.on_all_waves_complete:
                    self.on_all_waves_complete()
            else:
                if self.on_wave_complete:
                    self.on_wave_complete(self.current_wave)

    def cleanup(self):
        for enemy in self.enemies:
            if enemy:
                enemy.destroy()
        self.enemies.clear()
        self.spawn_queue.clear()
        self.wave_active = False
