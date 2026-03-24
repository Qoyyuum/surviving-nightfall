from ursina import Entity, Text, Button, color, destroy, camera, Vec3, Quad
import os

class MainMenu:
    def __init__(self, score_system):
        self.score_system = score_system
        self.ui_elements = []
        self.is_active = False
        
        self.on_start_game = None
        self.on_weapon_shop = None
        self.on_exit_game = None
        
    def show(self):
        self.is_active = True
        camera.position = Vec3(0, 5, -10)
        camera.rotation = Vec3(20, 0, 0)
        
        background_path = 'assets/images/menu_background.png'
        if os.path.exists(background_path):
            background = Entity(
                model='quad',
                texture=background_path,
                scale=(2, 1),
                position=(0, 0),
                z=1,
                parent=camera.ui
            )
            self.ui_elements.append(background)
        
        title = Text(
            text="SURVIVING NIGHTFALL",
            origin=(0, 0),
            scale=3,
            position=(0, 0.3),
            color=color.red
        )
        self.ui_elements.append(title)
        
        score_text = Text(
            text=f"Total Score: {self.score_system.total_score}",
            origin=(1, 1),  # Top right origin
            scale=1.2,
            position=(0.85, 0.48),  # Top right corner
            color=color.yellow
        )
        self.ui_elements.append(score_text)
        
        start_button = Button(
            text="Start Game",
            color=color.rgb32(60, 80, 45),
            scale=(0.3, 0.08),
            position=(0, -0.1),
            on_click=self._on_start_clicked,
        )
        self.ui_elements.append(start_button)
        
        shop_button = Button(
            text="Weapon Shop",
            color=color.rgb32(184,134,11),
            scale=(0.3, 0.08),
            position=(0, -0.2),
            on_click=self._on_shop_clicked
        )
        self.ui_elements.append(shop_button)
        
        exit_button = Button(
            text="Exit Game",
            color=color.rgb32(138, 3, 3),
            scale=(0.3, 0.08),
            position=(0, -0.3),
            on_click=self._on_exit_clicked
        )
        self.ui_elements.append(exit_button)
        
    def hide(self):
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        
    def _on_start_clicked(self):
        if self.on_start_game:
            self.on_start_game()
            
    def _on_shop_clicked(self):
        if self.on_weapon_shop:
            self.on_weapon_shop()
            
    def _on_exit_clicked(self):
        if self.on_exit_game:
            self.on_exit_game()
