from ursina import Text, Button, color, destroy, camera, Vec3, Func, Entity, time, mouse
from game.config import GameConfig
import math
import random


class WeaponShopUI:
    def __init__(self, score_system, audio_manager=None):
        self.score_system = score_system
        self.audio_manager = audio_manager
        self.ui_elements = []
        self.is_active = False
        self.weapon_models = []
        self.smoke_emitters = []
        self.weapon_buttons = {}  # Map buttons to weapon data
        self.description_panel = None
        self.description_title = None
        self.description_text = None
        self.description_stats = None

        self.on_back = None

    def show(self):
        self.is_active = True
        camera.position = Vec3(0, 5, -10)
        camera.rotation = Vec3(20, 0, 0)

        title = Text(
            text="WEAPON SHOP",
            origin=(0, 0),
            scale=2.5,
            position=(0, 0.4),
            color=color.rgb32(255, 255, 0),
        )
        self.ui_elements.append(title)

        self.score_text = Text(
            text=f"Available Score: {self.score_system.total_score}",
            origin=(1, 1),
            scale=1.5,
            position=(0.85, 0.48),
            color=color.rgb32(0, 255, 255),
        )
        self.ui_elements.append(self.score_text)

        # Map weapon names to their 3D model paths
        weapon_models_map = {
            "handgun": "assets/models/equipment/Pistol_1.obj",
            "shotgun": "assets/models/equipment/Shotgun_1.obj",
            "machine_gun": "cube",  # Placeholder
            "katana": "cube",  # Placeholder
            "chainsaw": "cube",  # Placeholder
            "bazooka": "cube",  # Placeholder
            "flamethrower": "cube",  # Placeholder
        }

        # Create grid layout (4 columns)
        weapons_list = list(GameConfig.WEAPONS.items())
        cols = 4
        rows = (len(weapons_list) + cols - 1) // cols
        
        grid_spacing_x = 0.28
        grid_spacing_y = 0.30
        start_x = -(cols - 1) * grid_spacing_x / 2
        start_y = 0.15
        
        for idx, (weapon_name, weapon_data) in enumerate(weapons_list):
            col = idx % cols
            row = idx // cols
            
            x_pos = start_x + (col * grid_spacing_x)
            y_pos = start_y - (row * grid_spacing_y)
            
            cost = weapon_data["cost"]
            is_unlocked = self.score_system.is_unlocked(weapon_name)
            can_afford = self.score_system.can_afford(weapon_name)
            
            # Create 3D model container
            model_container = Entity(
                parent=camera.ui,
                position=(x_pos, y_pos + 0.08, -1)
            )
            
            # Create rotating 3D weapon model
            model_path = weapon_models_map.get(weapon_name, "cube")
            weapon_model = Entity(
                parent=model_container,
                model=model_path,
                scale=0.05 if model_path.endswith('.obj') else 0.06,
                position=(0, 0, 0),
                rotation=(0, 0, 0)
            )
            
            # Set color for placeholder models
            if not model_path.endswith('.obj'):
                weapon_model.color = color.rgb32(150, 150, 150)
            
            weapon_model.rotation_speed = 40
            self.weapon_models.append(weapon_model)
            self.ui_elements.append(model_container)
            
            # Create smoke emitter behind model
            emitter = {
                'container': model_container,
                'particles': [],
                'spawn_timer': 0,
                'spawn_rate': 0.08,  # Spawn particle every 0.08 seconds
                'max_particles': 12,
                'is_unlocked': is_unlocked
            }
            self.smoke_emitters.append(emitter)
            
            # Create button below model (without description)
            weapon_title = weapon_name.replace('_', ' ').title()
            
            if is_unlocked:
                button_text = f"{weapon_title}\n[OWNED]"
                button_color = color.rgb32(50, 100, 50)
                button_enabled = False
            elif can_afford:
                button_text = f"{weapon_title}\n${cost} - BUY"
                button_color = color.rgb32(60, 60, 100)
                button_enabled = True
            else:
                button_text = f"{weapon_title}\n${cost} - LOCKED"
                button_color = color.rgb32(40, 40, 40)
                button_enabled = False
            
            # Create button with conditional on_click parameter
            button_params = {
                'text': button_text,
                'color': button_color,
                'highlight_color': color.rgb32(100, 100, 150) if button_enabled else button_color,
                'pressed_color': color.rgb32(120, 170, 255) if button_enabled else button_color,
                'scale': (0.13, 0.06),
                'position': (x_pos, y_pos - 0.03),
                'text_size': 0.6,
            }
            
            if button_enabled:
                button_params['on_click'] = Func(self._on_weapon_clicked, weapon_name)
            
            button = Button(**button_params)
            self.ui_elements.append(button)
            
            # Store weapon data for hover display
            self.weapon_buttons[button] = {
                'name': weapon_title,
                'cost': cost,
                'description': weapon_data['description'],
                'is_unlocked': is_unlocked,
                'can_afford': can_afford,
                'stats': weapon_data
            }

        # Create description panel on the left side
        panel_x = -0.75
        
        # Panel background (positioned behind text)
        self.description_panel = Entity(
            parent=camera.ui,
            model='quad',
            color=color.rgba(0.15, 0.15, 0.25, 0.95),
            scale=(0.35, 0.7),
            position=(panel_x, 0.0, 0.5)
        )
        self.ui_elements.append(self.description_panel)
        
        # Panel title (positioned in front of background)
        self.description_title = Text(
            text="Hover over a weapon",
            origin=(0, 0),
            scale=1.0,
            position=(panel_x, 0.3, -0.1),
            color=color.rgb32(255, 255, 150)
        )
        self.ui_elements.append(self.description_title)
        
        # Panel description (positioned in front of background)
        self.description_text = Text(
            text="to view details",
            origin=(0, 0),
            scale=0.8,
            position=(panel_x, 0.18, -0.1),
            color=color.rgb32(240, 240, 240)
        )
        self.ui_elements.append(self.description_text)
        
        # Panel stats (positioned in front of background)
        self.description_stats = Text(
            text="",
            origin=(0, 0),
            scale=0.75,
            position=(panel_x, -0.05, -0.1),
            color=color.rgb32(180, 220, 255)
        )
        self.ui_elements.append(self.description_stats)
        
        back_button = Button(
            text="Back to Menu",
            color=color.rgb32(150, 150, 150),
            scale=(0.3, 0.08),
            position=(0, -0.42),
            on_click=self._on_back_clicked,
        )
        self.ui_elements.append(back_button)

    def hide(self):
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        self.weapon_models.clear()
        self.weapon_buttons.clear()
        
        # Clean up smoke particles
        for emitter in self.smoke_emitters:
            for particle in emitter['particles']:
                if particle:
                    destroy(particle)
        self.smoke_emitters.clear()
    
    def update(self):
        if not self.is_active:
            return
        
        # Check for hovered weapon button
        hovered_weapon = None
        for button, weapon_data in self.weapon_buttons.items():
            if button.hovered:
                hovered_weapon = weapon_data
                break
        
        # Update description panel
        if hovered_weapon:
            self.description_title.text = hovered_weapon['name']
            self.description_text.text = hovered_weapon['description']
            
            # Build stats text
            stats_lines = []
            if hovered_weapon['is_unlocked']:
                stats_lines.append("Status: OWNED")
            elif hovered_weapon['can_afford']:
                stats_lines.append(f"Cost: ${hovered_weapon['cost']}")
                stats_lines.append("Status: AVAILABLE")
                stats_lines.append("Click to Purchase")
            else:
                stats_lines.append(f"Cost: ${hovered_weapon['cost']}")
                stats_lines.append("Status: LOCKED")
                stats_lines.append("Insufficient Funds")
            
            stats_lines.append("")
            stats = hovered_weapon['stats']
            if 'damage' in stats:
                stats_lines.append(f"Damage: {stats['damage']}")
            if 'fire_rate' in stats:
                stats_lines.append(f"Fire Rate: {stats['fire_rate']}s")
            if 'range' in stats:
                stats_lines.append(f"Range: {stats['range']}")
            if 'pellets' in stats:
                stats_lines.append(f"Pellets: {stats['pellets']}")
            if 'explosion_radius' in stats:
                stats_lines.append(f"Explosion Radius: {stats['explosion_radius']}")
            
            self.description_stats.text = "\n".join(stats_lines)
        else:
            self.description_title.text = "Hover over a weapon"
            self.description_text.text = "to view details"
            self.description_stats.text = ""
        
        # Rotate 3D weapon models
        for model in self.weapon_models:
            if model:
                model.rotation_y += model.rotation_speed * time.dt
                # Add hovering effect
                model.y = math.sin(time.time() * 1.5) * 0.008
        
        # Update smoke emitters
        for emitter in self.smoke_emitters:
            emitter['spawn_timer'] += time.dt
            
            # Spawn new smoke particles
            if emitter['spawn_timer'] >= emitter['spawn_rate'] and len(emitter['particles']) < emitter['max_particles']:
                emitter['spawn_timer'] = 0
                
                # Create smoke particle
                smoke_color = color.rgba(255, 240, 200, 180) if emitter['is_unlocked'] else color.rgba(240, 240, 255, 150)
                smoke = Entity(
                    parent=emitter['container'],
                    model='sphere',
                    color=smoke_color,
                    scale=0.01,
                    position=(
                        random.uniform(-0.03, 0.03),
                        -0.05,
                        0.02
                    )
                )
                smoke.velocity_y = random.uniform(0.08, 0.15)
                smoke.velocity_x = random.uniform(-0.02, 0.02)
                smoke.lifetime = random.uniform(1.2, 1.8)
                smoke.age = 0
                emitter['particles'].append(smoke)
            
            # Update existing smoke particles
            for smoke in emitter['particles'][:]:
                if not smoke:
                    emitter['particles'].remove(smoke)
                    continue
                
                smoke.age += time.dt
                
                # Move smoke upward and sideways
                smoke.y += smoke.velocity_y * time.dt
                smoke.x += smoke.velocity_x * time.dt
                
                # Fade out and grow
                progress = smoke.age / smoke.lifetime
                smoke.alpha = (1 - progress) * 0.6
                smoke.scale = 0.01 + progress * 0.02
                
                # Remove old particles
                if smoke.age >= smoke.lifetime:
                    destroy(smoke)
                    emitter['particles'].remove(smoke)

    def _on_weapon_clicked(self, weapon_name):
        if self.score_system.unlock_weapon(weapon_name):
            # Play purchase sound
            if self.audio_manager:
                self.audio_manager.play_sfx('weapon_purchase')
            self.hide()
            self.show()
        else:
            # Play button click for failed purchase
            if self.audio_manager:
                self.audio_manager.play_sfx('button_click')

    def _on_back_clicked(self):
        if self.audio_manager:
            self.audio_manager.play_sfx('button_click')
        if self.on_back:
            self.hide()
            self.on_back()
