from ursina import Entity, time, color, destroy, camera
from ursina.prefabs.first_person_controller import FirstPersonController
from game.config import GameConfig


class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(
            height=GameConfig.PLAYER_SIZE.y, speed=GameConfig.PLAYER_SPEED, **kwargs
        )

        self.max_health = GameConfig.PLAYER_MAX_HEALTH
        self.health = self.max_health

        self.is_alive = True
        self.current_weapon = None
        self.weapon_model = None  # Visual representation of weapon
        self.active_abilities = []
        self.game_manager = None  # Reference to game manager for audio

        self.damage_cooldown = 0
        self.damage_cooldown_time = 0.5

        # Position at spawn
        self.position = (0, GameConfig.PLAYER_SIZE.y / 2, 0)

    def take_damage(self, amount):
        if not self.is_alive or self.damage_cooldown > 0:
            return

        self.health -= amount
        self.damage_cooldown = self.damage_cooldown_time
        
        # Play player hit sound
        if self.game_manager and hasattr(self.game_manager, 'audio_manager'):
            self.game_manager.audio_manager.play_sfx('player_hit')

        if self.health <= 0:
            self.health = 0
            self.die()

    def heal(self, amount):
        if not self.is_alive:
            return

        self.health = min(self.health + amount, self.max_health)

    def die(self):
        self.is_alive = False
        self.visible = False
        
        # Play player death sound
        if self.game_manager and hasattr(self.game_manager, 'audio_manager'):
            self.game_manager.audio_manager.play_sfx('player_death')

    def equip_weapon(self, weapon):
        if self.current_weapon:
            destroy(self.current_weapon)
        self.current_weapon = weapon
        weapon.owner = self

        # Create visual weapon model using weapon's class properties
        if self.weapon_model:
            destroy(self.weapon_model)

        # Get visual properties from weapon class (with defaults)
        weapon_class = weapon.__class__
        visual_model = getattr(weapon_class, "visual_model", "cube")
        visual_color = getattr(weapon_class, "visual_color", color.white)
        visual_scale = getattr(weapon_class, "visual_scale", (0.1, 0.1, 0.3))
        visual_position = getattr(weapon_class, "visual_position", (0.4, -0.3, 0.5))
        visual_rotation = getattr(weapon_class, "visual_rotation", (-10, 0, 0))

        self.weapon_model = Entity(
            parent=camera,
            model=visual_model,
            color=visual_color,
            scale=visual_scale,
            position=visual_position,
            rotation=visual_rotation,
        )

    def add_ability(self, ability):
        self.active_abilities.append(ability)
        ability.activate(self)

    def update(self):
        if not self.is_alive:
            return

        # Check if game is paused
        if hasattr(self, 'game_manager') and self.game_manager.pause_menu.is_active:
            return

        # Call parent FirstPersonController update for movement
        super().update()

        if self.damage_cooldown > 0:
            self.damage_cooldown -= time.dt

        # Keep player within boundaries
        boundary = GameConfig.GROUND_SIZE / 2 - 2
        self.x = max(-boundary, min(boundary, self.x))
        self.z = max(-boundary, min(boundary, self.z))

        if self.current_weapon:
            self.current_weapon.update()

        for ability in self.active_abilities:
            ability.update()
