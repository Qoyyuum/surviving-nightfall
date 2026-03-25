from ursina import Text, Button, color, destroy, Entity, camera, Vec3, Func
from ursina.prefabs.button_list import ButtonList
from game.config import GameConfig

class WeaponShopUI:
    def __init__(self, score_system):
        self.score_system = score_system
        self.ui_elements = []
        self.is_active = False
        
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
            color=color.rgb32(255, 255, 0)
        )
        self.ui_elements.append(title)
        
        self.score_text = Text(
            text=f"Available Score: {self.score_system.total_score}",
            origin=(1, 1),  # Top right origin
            scale=1.5,
            position=(0.85, 0.48),  # Top right corner
            color=color.rgb32(0, 255, 255)
        )
        self.ui_elements.append(self.score_text)
        
        # Build button dictionary for ButtonList
        button_dict = {}
        for weapon_name, weapon_data in GameConfig.WEAPONS.items():
            cost = weapon_data["cost"]
            is_unlocked = self.score_system.is_unlocked(weapon_name)
            can_afford = self.score_system.can_afford(weapon_name)
            
            if is_unlocked:
                status = "✓ UNLOCKED"
            elif can_afford:
                status = f"${cost} - Click to Buy"
            else:
                status = f"${cost} - LOCKED"
            
            display_name = f"{weapon_name.replace('_', ' ').title()}: {weapon_data['description']} - {status}"
            
            # Only enable if can afford and not unlocked
            if can_afford and not is_unlocked:
                button_dict[display_name] = Func(self._on_weapon_clicked, weapon_name)
            else:
                button_dict[display_name] = None
        
        # Create ButtonList
        self.weapon_list = ButtonList(
            button_dict,
            button_height=1.2,
            width=0.7,
            popup=False,
            color=color.rgb32(40, 40, 60),
            highlight_color=color.rgb32(80, 80, 120),
            selected_color=color.rgb32(100, 150, 255)
        )
        self.weapon_list.position = (0, 0.15)
        self.ui_elements.append(self.weapon_list)
            
        back_button = Button(
            text="Back to Menu",
            color=color.rgb32(150, 150, 150),
            scale=(0.3, 0.08),
            position=(0, -0.42),
            on_click=self._on_back_clicked
        )
        self.ui_elements.append(back_button)
        
    def hide(self):
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        
    def _on_weapon_clicked(self, weapon_name):
        if self.score_system.unlock_weapon(weapon_name):
            self.hide()
            self.show()
            
    def _on_back_clicked(self):
        if self.on_back:
            self.hide()
            self.on_back()
