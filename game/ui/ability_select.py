from ursina import Text, color, destroy, time, Entity, Button, Vec3, camera
import random
import math


class AbilitySelectUI:
    def __init__(self):
        self.ui_elements = []
        self.is_active = False
        self.selected_ability = None
        self.timer = 0
        self.max_time = 60.0
        self.ability_models = []
        self.smoke_emitters = []

        self.on_ability_selected = None
        self.on_timeout = None

    def show(self, available_abilities):
        self.is_active = True
        self.timer = self.max_time
        self.selected_ability = None

        choices = random.sample(available_abilities, min(3, len(available_abilities)))

        title = Text(
            text="LEVEL UP! Choose an Ability",
            origin=(0, 0),
            scale=2,
            position=(0, 0.35),
            color=color.rgb32(255, 255, 0),
        )
        self.ui_elements.append(title)

        self.timer_text = Text(
            text="",
            origin=(0, 0),
            scale=1.5,
            position=(0, 0.25),
            color=color.rgb32(255, 255, 255),
        )
        self.ui_elements.append(self.timer_text)

        # Create horizontal layout with 3D models and buttons
        button_spacing = 0.35
        start_x = -button_spacing
        
        for i, ability in enumerate(choices):
            x_pos = start_x + (i * button_spacing)
            
            # Create ability name text
            ability_name = ability.name
            if hasattr(ability, "level") and ability.level > 1:
                ability_name += f" (Lv{ability.level})"
            
            # Create large clickable button behind everything
            button = Button(
                text='',
                color=color.rgba(0.1, 0.1, 0.1, 0.8),
                highlight_color=color.rgba(0.15, 0.15, 0.15, 0.9),
                pressed_color=color.rgba(0.2, 0.2, 0.25, 0.95),
                scale=(0.2, 0.45),
                position=(x_pos, 0.05, 1),
                on_click=lambda a=ability: self._on_ability_clicked(a)
            )
            self.ui_elements.append(button)
            
            # Create 3D model container (positioned above button)
            model_container = Entity(
                parent=camera.ui,
                position=(x_pos, 0.15, -1)
            )
            
            # Create rotating 3D model using ability's UI properties
            ability_model = Entity(
                parent=model_container,
                model=ability.ui_model,
                color=color.rgb32(*ability.ui_color),
                scale=0.08,
                position=(0, 0, 0)
            )
            ability_model.rotation_speed = 50
            self.ability_models.append(ability_model)
            self.ui_elements.append(model_container)
            
            # Create smoke emitter behind model
            emitter = {
                'container': model_container,
                'particles': [],
                'spawn_timer': 0,
                'spawn_rate': 0.08,  # Spawn particle every 0.08 seconds
                'max_particles': 15
            }
            self.smoke_emitters.append(emitter)
            
            # Create ability name text (positioned in front of button)
            name_text = Text(
                text=ability_name,
                origin=(0, 0),
                scale=1.0,
                position=(x_pos, -0.05, -0.1),
                color=color.rgb32(200, 200, 255)
            )
            self.ui_elements.append(name_text)
            
            # Create description text below name
            desc_text = Text(
                text=ability.description,
                origin=(0, 0),
                scale=0.8,
                position=(x_pos, -0.12),
                color=color.rgb32(200, 200, 200),
                wordwrap=12
            )
            self.ui_elements.append(desc_text)

    def hide(self):
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        self.ability_models.clear()
        
        # Clean up smoke particles
        for emitter in self.smoke_emitters:
            for particle in emitter['particles']:
                if particle:
                    destroy(particle)
        self.smoke_emitters.clear()

    def update(self):
        if not self.is_active:
            return

        self.timer -= time.dt

        if self.timer_text:
            self.timer_text.text = f"Time: {int(self.timer)}s"

        if self.timer <= 0:
            if self.on_timeout:
                self.on_timeout()
            self.hide()
        
        # Rotate 3D models
        for model in self.ability_models:
            if model:
                model.rotation_y += model.rotation_speed * time.dt
                # Add hovering effect
                model.y = math.sin(time.time() * 2) * 0.01
        
        # Update smoke emitters
        for emitter in self.smoke_emitters:
            emitter['spawn_timer'] += time.dt
            
            # Spawn new smoke particles
            if emitter['spawn_timer'] >= emitter['spawn_rate'] and len(emitter['particles']) < emitter['max_particles']:
                emitter['spawn_timer'] = 0
                
                # Create smoke particle
                smoke = Entity(
                    parent=emitter['container'],
                    model='sphere',
                    color=color.rgba(255, 255, 255, 160),
                    scale=0.012,
                    position=(
                        random.uniform(-0.04, 0.04),
                        -0.06,
                        0.02
                    )
                )
                smoke.velocity_y = random.uniform(0.1, 0.18)
                smoke.velocity_x = random.uniform(-0.025, 0.025)
                smoke.lifetime = random.uniform(1.0, 1.6)
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
                smoke.alpha = (1 - progress) * 0.65
                smoke.scale = 0.012 + progress * 0.025
                
                # Remove old particles
                if smoke.age >= smoke.lifetime:
                    destroy(smoke)
                    emitter['particles'].remove(smoke)

    def _on_ability_clicked(self, ability):
        self.selected_ability = ability
        if self.on_ability_selected:
            self.on_ability_selected(ability)
        self.hide()
