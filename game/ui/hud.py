from ursina import Text, Entity, color, destroy

class HUD:
    def __init__(self, player, xp_system, wave_manager):
        self.player = player
        self.xp_system = xp_system
        self.wave_manager = wave_manager
        self.ui_elements = []
        self.is_active = False
        
    def show(self):
        self.is_active = True
        
        self.health_text = Text(
            text="",
            position=(-0.85, 0.45),
            scale=1.5,
            color=color.red,
            origin=(-0.5, 0)
        )
        self.ui_elements.append(self.health_text)
        
        self.xp_text = Text(
            text="",
            position=(-0.85, -0.45),
            scale=1.2,
            color=color.cyan,
            origin=(-0.5, 0)
        )
        self.ui_elements.append(self.xp_text)
        
        self.wave_text = Text(
            text="",
            position=(0, 0.45),
            scale=2,
            color=color.white,
            origin=(0, 0)
        )
        self.ui_elements.append(self.wave_text)
        
        self.enemies_text = Text(
            text="",
            position=(0, 0.4),
            scale=1.2,
            color=color.orange,
            origin=(0, 0)
        )
        self.ui_elements.append(self.enemies_text)
        
        self.weapon_text = Text(
            text="",
            position=(0.85, 0.45),
            scale=1.2,
            color=color.yellow,
            origin=(0.5, 0)
        )
        self.ui_elements.append(self.weapon_text)
        
    def hide(self):
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        
    def update(self):
        if not self.is_active:
            return
            
        if self.health_text:
            self.health_text.text = f"HP: {int(self.player.health)}/{self.player.max_health}"
            
        if self.xp_text:
            xp_progress = int(self.xp_system.get_xp_progress() * 100)
            self.xp_text.text = f"Level {self.xp_system.current_level} | XP: {xp_progress}%"
            
        if self.wave_text:
            self.wave_text.text = f"Wave {self.wave_manager.current_wave}/5"
            
        if self.enemies_text:
            total_enemies = len(self.wave_manager.enemies) + len(self.wave_manager.spawn_queue)
            self.enemies_text.text = f"Enemies: {total_enemies}"
            
        if self.weapon_text and self.player.current_weapon:
            self.weapon_text.text = f"Weapon: {self.player.current_weapon.name}"
