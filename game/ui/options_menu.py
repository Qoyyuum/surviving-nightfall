from ursina import Entity, Text, Button, color, destroy, camera, Slider, mouse
import os


class OptionsMenu:
    """Options menu for audio and game settings"""
    
    def __init__(self, audio_manager):
        self.audio_manager = audio_manager
        self.ui_elements = []
        self.is_active = False
        
        # Callbacks
        self.on_back = None
        
        # UI references
        self.sfx_slider = None
        self.music_slider = None
        self.sfx_mute_button = None
        self.music_mute_button = None
    
    def show(self):
        """Display the options menu"""
        self.is_active = True
        mouse.locked = False
        
        # Background overlay
        background_path = "assets/images/menu_background.png"
        if os.path.exists(background_path):
            background = Entity(
                model="quad",
                texture=background_path,
                scale=(2, 1),
                position=(0, 0),
                z=1,
                parent=camera.ui,
            )
            self.ui_elements.append(background)
        
        # Title
        title = Text(
            text="OPTIONS",
            origin=(0, 0),
            scale=3,
            position=(0, 0.4),
            color=color.rgb32(255, 200, 0),
            parent=camera.ui
        )
        self.ui_elements.append(title)
        
        # Sound Effects Section
        sfx_label = Text(
            text="Sound Effects Volume",
            origin=(0, 0),
            scale=1.2,
            position=(0, 0.2),
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
            dynamic=True,
            position=(-0.2, 0.12),
            width=0.4,
            height=0.03,
            parent=camera.ui
        )
        self.sfx_slider.on_value_changed = self._on_sfx_volume_changed
        self.ui_elements.append(self.sfx_slider)
        
        # SFX Volume Text
        self.sfx_volume_text = Text(
            text=f"{int(self.audio_manager.sfx_volume * 100)}%",
            origin=(0, 0),
            scale=1,
            position=(0.25, 0.12),
            color=color.cyan,
            parent=camera.ui
        )
        self.ui_elements.append(self.sfx_volume_text)
        
        # SFX Mute Button
        sfx_mute_text = "Unmute SFX" if self.audio_manager.sfx_muted else "Mute SFX"
        sfx_mute_color = color.rgb32(60, 80, 45) if not self.audio_manager.sfx_muted else color.rgb32(138, 3, 3)
        
        self.sfx_mute_button = Button(
            text=sfx_mute_text,
            color=sfx_mute_color,
            scale=(0.2, 0.05),
            position=(0, 0.03),
            on_click=self._on_sfx_mute_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(self.sfx_mute_button)
        
        # Background Music Section
        music_label = Text(
            text="Background Music Volume",
            origin=(0, 0),
            scale=1.2,
            position=(0, -0.08),
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
            dynamic=True,
            position=(-0.2, -0.16),
            width=0.4,
            height=0.03,
            parent=camera.ui
        )
        self.music_slider.on_value_changed = self._on_music_volume_changed
        self.ui_elements.append(self.music_slider)
        
        # Music Volume Text
        self.music_volume_text = Text(
            text=f"{int(self.audio_manager.music_volume * 100)}%",
            origin=(0, 0),
            scale=1,
            position=(0.25, -0.16),
            color=color.cyan,
            parent=camera.ui
        )
        self.ui_elements.append(self.music_volume_text)
        
        # Music Mute Button
        music_mute_text = "Unmute Music" if self.audio_manager.music_muted else "Mute Music"
        music_mute_color = color.rgb32(60, 80, 45) if not self.audio_manager.music_muted else color.rgb32(138, 3, 3)
        
        self.music_mute_button = Button(
            text=music_mute_text,
            color=music_mute_color,
            scale=(0.2, 0.05),
            position=(0, -0.25),
            on_click=self._on_music_mute_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(self.music_mute_button)
        
        # Back Button
        back_button = Button(
            text="Back",
            color=color.rgb32(60, 80, 45),
            scale=(0.25, 0.07),
            position=(0, -0.38),
            on_click=self._on_back_clicked,
            parent=camera.ui
        )
        self.ui_elements.append(back_button)
    
    def hide(self):
        """Hide the options menu"""
        self.is_active = False
        for element in self.ui_elements:
            if element:
                destroy(element)
        self.ui_elements.clear()
        
        self.sfx_slider = None
        self.music_slider = None
        self.sfx_mute_button = None
        self.music_mute_button = None
    
    def _on_sfx_volume_changed(self):
        """Handle SFX volume slider change"""
        if self.sfx_slider:
            volume = self.sfx_slider.value / 100.0
            self.audio_manager.set_sfx_volume(volume)
            
            # Update volume text
            if self.sfx_volume_text:
                self.sfx_volume_text.text = f"{int(volume * 100)}%"
            
            # Play a test sound
            self.audio_manager.play_sfx('button_click', volume_multiplier=0.5)
    
    def _on_music_volume_changed(self):
        """Handle music volume slider change"""
        if self.music_slider:
            volume = self.music_slider.value / 100.0
            self.audio_manager.set_music_volume(volume)
            
            # Update volume text
            if self.music_volume_text:
                self.music_volume_text.text = f"{int(volume * 100)}%"
    
    def _on_sfx_mute_clicked(self):
        """Handle SFX mute button click"""
        muted = self.audio_manager.toggle_sfx_mute()
        
        # Update button appearance
        if self.sfx_mute_button:
            self.sfx_mute_button.text = "Unmute SFX" if muted else "Mute SFX"
            self.sfx_mute_button.color = color.rgb32(138, 3, 3) if muted else color.rgb32(60, 80, 45)
        
        # Play test sound if unmuting
        if not muted:
            self.audio_manager.play_sfx('button_click', volume_multiplier=0.5)
    
    def _on_music_mute_clicked(self):
        """Handle music mute button click"""
        muted = self.audio_manager.toggle_music_mute()
        
        # Update button appearance
        if self.music_mute_button:
            self.music_mute_button.text = "Unmute Music" if muted else "Mute Music"
            self.music_mute_button.color = color.rgb32(138, 3, 3) if muted else color.rgb32(60, 80, 45)
        
        # Play button click sound
        self.audio_manager.play_sfx('button_click', volume_multiplier=0.5)
    
    def _on_back_clicked(self):
        """Handle back button click"""
        self.audio_manager.play_sfx('button_click')
        
        if self.on_back:
            self.on_back()
