from ursina import Text, Button, color, destroy, Entity, camera, Vec3
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
            color=color.yellow
        )
        self.ui_elements.append(title)
        
        self.score_text = Text(
            text=f"Available Score: {self.score_system.total_score}",
            origin=(1, 1),  # Top right origin
            scale=1.5,
            position=(0.85, 0.48),  # Top right corner
            color=color.cyan
        )
        self.ui_elements.append(self.score_text)
        
        y_start = 0.22
        y_spacing = 0.075
        
        print(f"Creating weapon shop with {len(GameConfig.WEAPONS)} weapons")
        
        for i, (weapon_name, weapon_data) in enumerate(GameConfig.WEAPONS.items()):
            y_pos = y_start - (i * y_spacing)
            
            cost = weapon_data["cost"]
            is_unlocked = self.score_system.is_unlocked(weapon_name)
            can_afford = self.score_system.can_afford(weapon_name)
            
            if is_unlocked:
                status = "[UNLOCKED]"
                btn_color = color.green
            elif can_afford:
                status = f"Cost: {cost}"
                btn_color = color.blue
            else:
                status = f"Cost: {cost} [LOCKED]"
                btn_color = color.red
                
            button_text = f"{weapon_name.replace('_', ' ').title()}: {weapon_data['description']} - {weapon_data['cost']} {status}"
            
            # print(f"  Creating button {i}: {weapon_name} at y={y_pos}, unlocked={is_unlocked}, affordable={can_afford}")
            
            button = Button(
                text=button_text,
                color=btn_color,
                scale=(0.6, 0.05),
                position=(0, y_pos),
                origin=(0, 0),
                on_click=lambda w=weapon_name: self._on_weapon_clicked(w),
                enabled=True,
                text_size=0.75
            )
            self.ui_elements.append(button)
            print(f"    Button created at ({0}, {y_pos}), scale=(0.6, 0.05)")
            
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
