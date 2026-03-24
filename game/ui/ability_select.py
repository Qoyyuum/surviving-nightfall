from ursina import Text, Button, color, destroy, Entity
import random

class AbilitySelectUI:
    def __init__(self):
        self.ui_elements = []
        self.is_active = False
        self.selected_ability = None
        self.timer = 0
        self.max_time = 60.0
        
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
            color=color.yellow
        )
        self.ui_elements.append(title)
        
        self.timer_text = Text(
            text="",
            origin=(0, 0),
            scale=1.5,
            position=(0, 0.25),
            color=color.white
        )
        self.ui_elements.append(self.timer_text)
        
        y_positions = [0.1, -0.05, -0.2]
        
        for i, ability in enumerate(choices):
            ability_name = ability.name
            if hasattr(ability, 'level') and ability.level > 1:
                ability_name += f" (Level {ability.level})"
                
            button = Button(
                text=f"{ability_name}\n{ability.description}",
                color=color.rgb(100, 50, 150),
                scale=(0.5, 0.12),
                position=(0, y_positions[i]),
                on_click=lambda a=ability: self._on_ability_clicked(a)
            )
            self.ui_elements.append(button)
            
    def hide(self):
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        
    def update(self):
        if not self.is_active:
            return
            
        self.timer -= 1/60.0
        
        if self.timer_text:
            self.timer_text.text = f"Time: {int(self.timer)}s"
            
        if self.timer <= 0:
            if self.on_timeout:
                self.on_timeout()
            self.hide()
            
    def _on_ability_clicked(self, ability):
        self.selected_ability = ability
        if self.on_ability_selected:
            self.on_ability_selected(ability)
        self.hide()
