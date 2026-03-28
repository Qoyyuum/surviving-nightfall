from ursina import Audio, destroy
from game.config import GameConfig
import os


class AudioManager:
    """Manages all game audio including sound effects and background music"""
    
    def __init__(self):
        # Volume settings (0.0 to 1.0)
        self.sfx_volume = 0.7
        self.music_volume = 0.5
        
        # Mute toggles
        self.sfx_muted = False
        self.music_muted = False
        
        # Current playing music
        self.current_music = None
        self.current_music_name = None
        
        # Sound effect cache
        self.sfx_cache = {}
        
        # Load audio paths from config
        self.sfx_paths = GameConfig.AUDIO_SFX_PATHS
        self.music_paths = GameConfig.AUDIO_MUSIC_PATHS
    
    def play_sfx(self, sfx_name, volume_multiplier=1.0):
        """Play a sound effect"""
        if self.sfx_muted:
            return
        
        if sfx_name not in self.sfx_paths:
            return
        
        path = self.sfx_paths[sfx_name]
        
        # Check if file exists
        if not os.path.exists(path):
            return
        
        try:
            # Calculate final volume
            final_volume = self.sfx_volume * volume_multiplier
            
            # Play the sound effect
            sfx = Audio(path, loop=False, autoplay=True, volume=final_volume)
            
            # Audio will auto-destroy after playing
        except Exception as e:
            print(f"Failed to play sfx '{sfx_name}' at path '{path}': {e}")
    
    def play_music(self, music_name, loop=True):
        """Play background music"""
        if music_name == self.current_music_name:
            return
        
        # Validate music exists before stopping current music
        if music_name not in self.music_paths:
            return
        
        path = self.music_paths[music_name]
        
        # Check if file exists
        if not os.path.exists(path):
            return
        
        # Stop current music only after validation
        self.stop_music()
        
        try:
            volume = 0 if self.music_muted else self.music_volume
            self.current_music = Audio(path, loop=loop, autoplay=True, volume=volume)
            self.current_music_name = music_name
        except Exception as e:
            print(f"Failed to play music '{music_name}' at path '{path}': {e}")
    
    def stop_music(self):
        """Stop currently playing music"""
        if self.current_music:
            destroy(self.current_music)
            self.current_music = None
            self.current_music_name = None
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        
        # Update current music volume if playing
        if self.current_music and not self.music_muted:
            self.current_music.volume = self.music_volume
    
    def toggle_sfx_mute(self):
        """Toggle sound effects mute"""
        self.sfx_muted = not self.sfx_muted
        return self.sfx_muted
    
    def toggle_music_mute(self):
        """Toggle music mute"""
        self.music_muted = not self.music_muted
        
        # Update current music volume
        if self.current_music:
            self.current_music.volume = 0 if self.music_muted else self.music_volume
        
        return self.music_muted
    
    def set_sfx_mute(self, muted):
        """Set sound effects mute state"""
        self.sfx_muted = muted
    
    def set_music_mute(self, muted):
        """Set music mute state"""
        self.music_muted = muted
        
        # Update current music volume
        if self.current_music:
            self.current_music.volume = 0 if self.music_muted else self.music_volume
    
    def cleanup(self):
        """Clean up all audio resources"""
        self.stop_music()
        self.sfx_cache.clear()
