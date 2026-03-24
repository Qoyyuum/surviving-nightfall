from ursina import Text, Button, color, destroy, camera, Vec3

class GameOverUI:
    def __init__(self):
        self.ui_elements = []
        self.is_active = False
        
        self.on_return_to_menu = None
        
    def show(self, victory, session_score, total_score):
        self.is_active = True
        camera.position = Vec3(0, 5, -10)
        camera.rotation = Vec3(20, 0, 0)
        
        if victory:
            title_text = "VICTORY!"
            title_color = color.green
            subtitle = "You survived all 5 waves!"
        else:
            title_text = "GAME OVER"
            title_color = color.red
            subtitle = "You have fallen..."
            
        title = Text(
            text=title_text,
            origin=(0, 0),
            scale=3,
            position=(0, 0.3),
            color=title_color
        )
        self.ui_elements.append(title)
        
        subtitle_text = Text(
            text=subtitle,
            origin=(0, 0),
            scale=1.5,
            position=(0, 0.2),
            color=color.white
        )
        self.ui_elements.append(subtitle_text)
        
        session_text = Text(
            text=f"Session Score: {session_score}",
            origin=(0, 0),
            scale=1.8,
            position=(0, 0.08),
            color=color.yellow
        )
        self.ui_elements.append(session_text)
        
        total_text = Text(
            text=f"Total Score: {total_score}",
            origin=(0, 0),
            scale=1.5,
            position=(0, -0.02),
            color=color.cyan
        )
        self.ui_elements.append(total_text)
        
        return_button = Button(
            text="Return to Menu",
            color=color.rgb32(100, 100, 200),
            scale=(0.35, 0.1),
            position=(0, -0.2),
            on_click=self._on_return_clicked
        )
        self.ui_elements.append(return_button)
        
    def hide(self):
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        
    def _on_return_clicked(self):
        if self.on_return_to_menu:
            self.on_return_to_menu()
