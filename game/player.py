from ursina import Entity, Vec3, held_keys, time, color, destroy, camera
from ursina.prefabs.first_person_controller import FirstPersonController
from game.config import GameConfig

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(
            height=GameConfig.PLAYER_SIZE.y,
            speed=GameConfig.PLAYER_SPEED,
            **kwargs
        )
        
        self.max_health = GameConfig.PLAYER_MAX_HEALTH
        self.health = self.max_health
        
        self.is_alive = True
        self.current_weapon = None
        self.weapon_model = None  # Visual representation of weapon
        self.active_abilities = []
        
        self.damage_cooldown = 0
        self.damage_cooldown_time = 0.5
        
        # Position at spawn
        self.position = (0, GameConfig.PLAYER_SIZE.y / 2, 0)
        
    def take_damage(self, amount):
        if not self.is_alive or self.damage_cooldown > 0:
            return
            
        self.health -= amount
        self.damage_cooldown = self.damage_cooldown_time
        
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
        
    def equip_weapon(self, weapon):
        if self.current_weapon:
            destroy(self.current_weapon)
        self.current_weapon = weapon
        weapon.owner = self
        
        # Create visual weapon model
        if self.weapon_model:
            destroy(self.weapon_model)
        
        # Different shapes and colors for different weapons
        weapon_visuals = {
            "Handgun": {"model": "cube", "color": color.gray, "scale": (0.1, 0.15, 0.3)},
            "Shotgun": {"model": "cube", "color": color.brown, "scale": (0.15, 0.2, 0.5)},
            "Machine Gun": {"model": "cube", "color": color.black, "scale": (0.12, 0.18, 0.4)},
            "Katana": {"model": "cube", "color": color.cyan, "scale": (0.05, 0.05, 0.8)},
            "Chainsaw": {"model": "cube", "color": color.orange, "scale": (0.2, 0.2, 0.4)},
            "Bazooka": {"model": "cube", "color": color.olive, "scale": (0.2, 0.25, 0.6)},
            "Flamethrower": {"model": "cube", "color": color.red, "scale": (0.15, 0.2, 0.5)}
        }
        
        visual = weapon_visuals.get(weapon.name, {"model": "cube", "color": color.white, "scale": (0.1, 0.1, 0.3)})
        
        self.weapon_model = Entity(
            parent=camera,
            model=visual["model"],
            color=visual["color"],
            scale=visual["scale"],
            position=(0.4, -0.3, 0.5),  # Right side, lower, in front
            rotation=(-10, 0, 0)
        )
        
    def add_ability(self, ability):
        self.active_abilities.append(ability)
        ability.activate(self)
        
    def update(self):
        if not self.is_alive:
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
