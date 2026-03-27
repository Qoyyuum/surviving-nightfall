from ursina import Entity, Text, Button, color, destroy, camera, mouse


class ConfirmationDialog:
    def __init__(self):
        self.ui_elements = []
        self.on_confirm = None
        self.on_cancel = None
        
    def show(self, message, on_confirm=None, on_cancel=None):
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        
        # Semi-transparent overlay
        overlay = Button(
            color=color.rgba(0, 0, 0, 200),
            scale=(999, 999),
            z=-1,
            enabled=False,
            parent=camera.ui
        )
        self.ui_elements.append(overlay)
        
        # Dialog background
        dialog_bg = Button(
            color=color.rgb32(40, 40, 40),
            scale=(0.6, 0.3),
            position=(0, 0),
            enabled=False,
            parent=camera.ui
        )
        self.ui_elements.append(dialog_bg)
        
        # Warning message
        warning_text = Text(
            text=message,
            origin=(0, 0),
            scale=1.2,
            position=(0, 0.08),
            color=color.yellow,
            parent=camera.ui
        )
        self.ui_elements.append(warning_text)
        
        # Confirm button
        confirm_button = Button(
            text="Yes, Exit",
            color=color.rgb32(138, 3, 3),
            scale=(0.2, 0.06),
            position=(-0.12, -0.05),
            on_click=self._on_confirm_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(confirm_button)
        
        # Cancel button
        cancel_button = Button(
            text="Cancel",
            color=color.rgb32(60, 80, 45),
            scale=(0.2, 0.06),
            position=(0.12, -0.05),
            on_click=self._on_cancel_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(cancel_button)
    
    def hide(self):
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
    
    def _on_confirm_clicked(self):
        if self.on_confirm:
            self.on_confirm()
        self.hide()
    
    def _on_cancel_clicked(self):
        if self.on_cancel:
            self.on_cancel()
        self.hide()


class PauseMenu:
    def __init__(self):
        self.ui_elements = []
        self.is_active = False
        self.confirmation_dialog = ConfirmationDialog()
        
        self.on_resume = None
        self.on_exit_to_menu = None
    
    def _hide_elements(self):
        """Temporarily hide pause menu elements without destroying them"""
        for element in self.ui_elements:
            if element:
                element.enabled = False
                element.visible = False
    
    def _show_elements(self):
        """Restore visibility of pause menu elements"""
        for element in self.ui_elements:
            if element:
                element.enabled = True
                element.visible = True
    
    def show(self):
        if self.is_active:
            return
            
        self.is_active = True
        mouse.locked = False
        
        # Semi-transparent overlay
        overlay = Button(
            color=color.rgba(0, 0, 0, 150),
            scale=(999, 999),
            z=-1,
            enabled=False,
            parent=camera.ui
        )
        self.ui_elements.append(overlay)
        
        # Title
        title = Text(
            text="PAUSED",
            origin=(0, 0),
            scale=3,
            position=(0, 0.3),
            color=color.white,
            parent=camera.ui
        )
        self.ui_elements.append(title)
        
        # Resume button
        resume_button = Button(
            text="Resume",
            color=color.rgb32(60, 80, 45),
            scale=(0.3, 0.08),
            position=(0, 0.05),
            on_click=self._on_resume_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(resume_button)
        
        # Exit to Main Menu button
        exit_button = Button(
            text="Exit to Main Menu",
            color=color.rgb32(138, 3, 3),
            scale=(0.3, 0.08),
            position=(0, -0.08),
            on_click=self._on_exit_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(exit_button)
    
    def hide(self):
        if not self.is_active:
            return
            
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        mouse.locked = True
    
    def _on_resume_clicked(self):
        self.hide()
        if self.on_resume:
            self.on_resume()
    
    def _on_exit_clicked(self):
        # Hide pause menu elements while showing confirmation
        self._hide_elements()
        
        self.confirmation_dialog.show(
            message="Exit to Main Menu?\nAll progress and scores from\nthis run will be lost!",
            on_confirm=self._confirm_exit,
            on_cancel=self._on_cancel_exit
        )
    
    def _on_cancel_exit(self):
        # Restore pause menu elements when cancelled
        self._show_elements()
    
    def _confirm_exit(self):
        self.hide()
        if self.on_exit_to_menu:
            self.on_exit_to_menu()
