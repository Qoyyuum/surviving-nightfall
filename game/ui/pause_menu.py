from ursina import Entity, Text, Button, color, destroy, camera, mouse, Slider


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
    def __init__(self, audio_manager=None):
        self.audio_manager = audio_manager
        self.ui_elements = []
        self.is_active = False
        self.confirmation_dialog = ConfirmationDialog()
        
        self.on_resume = None
        self.on_exit_to_menu = None
        
        # UI references for audio controls
        self.sfx_slider = None
        self.music_slider = None
        self.sfx_volume_text = None
        self.music_volume_text = None
        self.sfx_mute_button = None
        self.music_mute_button = None
    
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
        
        # Audio controls (if audio_manager is available)
        if self.audio_manager:
            self._create_audio_controls()
    
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
    
    def _create_audio_controls(self):
        """Create audio control sliders and buttons"""
        # SFX Section Label
        sfx_label = Text(
            text="Sound Effects",
            origin=(0, 0),
            scale=1.2,
            position=(-0.35, -0.22),
            color=color.white,
            parent=camera.ui
        )
        self.ui_elements.append(sfx_label)
        
        # SFX Volume Slider
        self.sfx_slider = Slider(
            min=0,
            max=100,
            default=int(self.audio_manager.sfx_volume * 100),
            step=1,
            dynamic=False,
            position=(-0.45, -0.28),
            width=0.25,
            height=0.025,
            parent=camera.ui
        )
        self.sfx_slider.on_value_changed = self._on_sfx_volume_changed
        self.ui_elements.append(self.sfx_slider)
        
        # SFX Volume Text
        self.sfx_volume_text = Text(
            text=f"{int(self.audio_manager.sfx_volume * 100)}%",
            origin=(0, 0),
            scale=0.8,
            position=(-0.15, -0.28),
            color=color.cyan,
            parent=camera.ui
        )
        self.ui_elements.append(self.sfx_volume_text)
        
        # SFX Mute Button
        sfx_mute_text = "Unmute" if self.audio_manager.sfx_muted else "Mute"
        self.sfx_mute_button = Button(
            text=sfx_mute_text,
            color=color.rgb32(80, 80, 80),
            scale=(0.12, 0.04),
            position=(-0.05, -0.28),
            on_click=self._on_sfx_mute_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(self.sfx_mute_button)
        
        # Music Section Label
        music_label = Text(
            text="Music",
            origin=(0, 0),
            scale=1.2,
            position=(0.15, -0.22),
            color=color.white,
            parent=camera.ui
        )
        self.ui_elements.append(music_label)
        
        # Music Volume Slider
        self.music_slider = Slider(
            min=0,
            max=100,
            default=int(self.audio_manager.music_volume * 100),
            step=1,
            dynamic=False,
            position=(0.05, -0.28),
            width=0.25,
            height=0.025,
            parent=camera.ui
        )
        self.music_slider.on_value_changed = self._on_music_volume_changed
        self.ui_elements.append(self.music_slider)
        
        # Music Volume Text
        self.music_volume_text = Text(
            text=f"{int(self.audio_manager.music_volume * 100)}%",
            origin=(0, 0),
            scale=0.8,
            position=(0.35, -0.28),
            color=color.cyan,
            parent=camera.ui
        )
        self.ui_elements.append(self.music_volume_text)
        
        # Music Mute Button
        music_mute_text = "Unmute" if self.audio_manager.music_muted else "Mute"
        self.music_mute_button = Button(
            text=music_mute_text,
            color=color.rgb32(80, 80, 80),
            scale=(0.12, 0.04),
            position=(0.45, -0.28),
            on_click=self._on_music_mute_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(self.music_mute_button)
    
    def _on_sfx_volume_changed(self):
        """Handle SFX volume slider change"""
        if self.sfx_slider and self.audio_manager:
            volume = self.sfx_slider.value / 100.0
            self.audio_manager.set_sfx_volume(volume)
            
            # Update volume text
            if self.sfx_volume_text:
                self.sfx_volume_text.text = f"{int(volume * 100)}%"
            
            # Play a test sound
            self.audio_manager.play_sfx('button_click', volume_multiplier=0.5)
    
    def _on_music_volume_changed(self):
        """Handle music volume slider change"""
        if self.music_slider and self.audio_manager:
            volume = self.music_slider.value / 100.0
            self.audio_manager.set_music_volume(volume)
            
            # Update volume text
            if self.music_volume_text:
                self.music_volume_text.text = f"{int(volume * 100)}%"
    
    def _on_sfx_mute_clicked(self):
        """Handle SFX mute button click"""
        if self.audio_manager:
            muted = self.audio_manager.toggle_sfx_mute()
            
            # Update button text
            if self.sfx_mute_button:
                self.sfx_mute_button.text = "Unmute" if muted else "Mute"
    
    def _on_music_mute_clicked(self):
        """Handle music mute button click"""
        if self.audio_manager:
            muted = self.audio_manager.toggle_music_mute()
            
            # Update button text
            if self.music_mute_button:
                self.music_mute_button.text = "Unmute" if muted else "Mute"
