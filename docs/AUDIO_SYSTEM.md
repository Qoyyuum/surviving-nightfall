# Audio System Documentation

## Overview

The audio system for Surviving Nightfall provides comprehensive sound effects and background music support with independent volume controls and mute toggles.

## Features

- **Independent Volume Controls**: Separate sliders for sound effects and background music (0-100%)
- **Mute Toggles**: Independent mute buttons for SFX and music
- **Options Menu**: Accessible from the main menu with an "Options" button
- **Audio Hooks**: Sound effects and music integrated throughout the game

## Audio Manager

The `AudioManager` class (`game/systems/audio_manager.py`) handles all audio playback:

- Volume management (0.0 to 1.0 scale)
- Mute state management
- Sound effect playback
- Background music playback with looping
- Automatic file existence checking

## Options Menu

Access the options menu from the main menu by clicking the "Options" button.

### Controls

- **Sound Effects Volume Slider**: Adjust SFX volume from 0-100%
- **Background Music Volume Slider**: Adjust music volume from 0-100%
- **Mute SFX Button**: Toggle sound effects on/off
- **Mute Music Button**: Toggle background music on/off
- **Back Button**: Return to main menu

## Audio File Structure

All audio files should be placed in the following directories:

### Sound Effects
Location: `assets/audio/sfx/`

### Background Music
Location: `assets/audio/music/`

## Required Sound Effects

The following sound effects are prepared and ready for audio files:

### Weapon Sounds
- `handgun_fire.wav` - Handgun firing sound
- `shotgun_fire.wav` - Shotgun firing sound
- `machine_gun_fire.wav` - Machine gun firing sound
- `katana_swing.wav` - Katana swing sound
- `chainsaw_fire.wav` - Chainsaw attack sound
- `bazooka_fire.wav` - Bazooka firing sound
- `flamethrower_fire.wav` - Flamethrower firing sound

### Monster Sounds
- `zombie_growl.wav` - Basic zombie sound
- `fast_zombie_growl.wav` - Fast zombie sound
- `tank_zombie_growl.wav` - Tank zombie sound
- `boss_zombie_growl.wav` - Boss zombie sound

### Combat Sounds
- `monster_hit.wav` - When a monster is hit
- `monster_death.wav` - When a monster dies
- `player_hit.wav` - When the player takes damage
- `player_death.wav` - When the player dies

### Game Event Sounds
- `game_over.wav` - Game over screen
- `game_start.wav` - When starting a new game
- `game_pause.wav` - When pausing the game
- `game_resume.wav` - When resuming from pause

### UI Sounds
- `button_click.wav` - Button click sound
- `weapon_purchase.wav` - Weapon shop purchase sound

### Ability Sounds
- `arc_lightning.wav` - Arc lightning ability activation
- `healing_orb_collect.wav` - Healing orb collection
- `xp_orb_collect.wav` - XP orb collection

### Wave Events
- `wave_complete.wav` - Wave completion sound

## Required Background Music

The following background music tracks are prepared:

### Menu Music
- `menu_theme.mp3` - Main menu, weapon shop, and options screen background music

### Battle Music
- `battle_theme.mp3` - Standard wave battle music (waves 1-4)

### Boss Music
- `boss_theme.mp3` - Final wave boss battle music (wave 5)

## Music Transitions

The game automatically handles music transitions:

1. **Main Menu**: Plays `menu_theme.mp3` when entering the main menu
2. **Game Start**: Switches to `battle_theme.mp3` when starting a game
3. **Final Wave**: Switches to `boss_theme.mp3` when wave 5 begins
4. **Game Over**: Stops all music when the game ends
5. **Return to Menu**: Resumes `menu_theme.mp3` when returning to the main menu

## Implementation Details

### Adding Audio to New Features

To add audio to new game features:

1. **Add the sound path** to `AudioManager.sfx_paths` or `AudioManager.music_paths`
2. **Call the audio manager** at the appropriate event:
   ```python
   self.audio_manager.play_sfx('sound_name')
   # or
   self.audio_manager.play_music('music_name')
   ```

### Weapon Audio

All weapons automatically play their assigned sound effect when fired. To add audio to a new weapon:

1. Add the sound file path to `AudioManager.sfx_paths`
2. Set the `sound_effect` class attribute in the weapon class:
   ```python
   class NewWeapon(BaseWeapon):
       sound_effect = 'new_weapon_fire'
   ```

### Volume Control

The audio system respects volume settings:
- Sound effects use `sfx_volume` (0.0 to 1.0)
- Background music uses `music_volume` (0.0 to 1.0)
- Muted audio will not play regardless of volume

## Audio File Recommendations

### Sound Effects
- **Format**: WAV (uncompressed for low latency)
- **Sample Rate**: 44.1 kHz or 48 kHz
- **Bit Depth**: 16-bit or 24-bit
- **Channels**: Mono or Stereo

### Background Music
- **Format**: MP3 (compressed for smaller file size)
- **Bitrate**: 192 kbps or higher
- **Sample Rate**: 44.1 kHz
- **Channels**: Stereo

## Current Status

The audio system is **fully implemented** with all hooks in place. The game will function normally without audio files, but will play sounds when the appropriate files are added to the `assets/audio/` directory structure.

To enable audio:
1. Create the directory structure: `assets/audio/sfx/` and `assets/audio/music/`
2. Add audio files with the exact names listed above
3. The audio system will automatically detect and play them

## Testing

To test the audio system:
1. Open the Options menu from the main menu
2. Adjust volume sliders and verify the percentage updates
3. Toggle mute buttons and verify button text/color changes
4. Play the game and verify audio hooks trigger at appropriate times (when audio files are present)
