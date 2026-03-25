from ursina import Text, Button, color, destroy, Entity
from ursina.prefabs.button_group import ButtonGroup
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
            color=color.rgb32(255, 255, 0)
        )
        self.ui_elements.append(title)
        
        self.timer_text = Text(
            text="",
            origin=(0, 0),
            scale=1.5,
            position=(0, 0.25),
            color=color.rgb32(255, 255, 255)
        )
        self.ui_elements.append(self.timer_text)
        
        # Build options list for ButtonGroup
        options = []
        self.ability_map = {}  # Map display names to abilities
        
        for ability in choices:
            ability_name = ability.name
            if hasattr(ability, 'level') and ability.level > 1:
                ability_name += f" (Lv{ability.level})"
            
            display_text = f"{ability_name}: {ability.description}"
            options.append(display_text)
            self.ability_map[display_text] = ability
        
        # Create ButtonGroup for ability selection
        self.ability_group = ButtonGroup(
            options=options,
            min_selection=0,
            max_selection=1,
            origin=(0, 0),
            spacing=(0, 0.025),
            max_x=1
        )
        self.ability_group.position = (0, 0.05)
        self.ability_group.on_value_changed = self._on_ability_group_changed
        self.ability_group.selected_color = color.rgb32(100, 150, 255)
        self.ability_group.highlight_selected_color = color.rgb32(120, 170, 255)
        self.ui_elements.append(self.ability_group)
            
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
            
    def _on_ability_group_changed(self):
        """Called when ButtonGroup selection changes"""
        if hasattr(self, 'ability_group') and self.ability_group.selected:
            selected_text = self.ability_group.selected[0].value
            ability = self.ability_map.get(selected_text)
            if ability:
                self.selected_ability = ability
                if self.on_ability_selected:
                    self.on_ability_selected(ability)
                self.hide()
    
    def _on_ability_clicked(self, ability):
        self.selected_ability = ability
        if self.on_ability_selected:
            self.on_ability_selected(ability)
        self.hide()
