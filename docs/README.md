# Surviving Nightfall

A 3D third-person bullet hell survival game built with Python and Ursina Game Engine.

## Game Description

**Surviving Nightfall** is a roguelike permadeath survival game where you fight through waves of supernatural enemies in an endless night. Armed with various weapons and special abilities, survive 5 increasingly difficult waves to claim victory.

### Story

You are thrown into a world of neverending darkness called "Surviving Nightfall." Vampires, Zombies, Ghosts, Goblins, Minotaurs, and various enemies with different abilities are out to kill every human on earth. Survive the longest night by shooting, leveling up, and unlocking powerful weapons.

---

## Features

### Gameplay
- **5 Wave Progression System** - Each wave increases in difficulty and enemy variety
- **Roguelike Permadeath** - Start fresh each game, but keep your unlocked weapons
- **Third-Person Shooter Controls** - WASD movement, mouse-look aiming, left-click shooting
- **XP & Leveling System** - Gain experience from kills to level up and choose abilities
- **Persistent Score System** - Accumulate score across sessions to unlock new weapons

### Enemies (5 Types)
- **Zombie** - Basic melee enemy
- **Ghost** - Can occasionally dodge bullets (30% chance)
- **Vampire** - Alternates between walking and speed bursts
- **Goblin** - Small, jumps toward the player
- **Minotaur** - High HP boss enemy (Wave 5 only)

### Weapons (7 Total)
- **Handgun** (Starting weapon) - Reliable single-shot
- **Shotgun** - Fires 5 pellets in spread pattern
- **Machine Gun** - Rapid fire with slight accuracy penalty
- **Dual Wield Katana** - Melee slashes with bleed damage
- **Chainsaw** - Continuous melee damage with pushback
- **Bazooka** - Explosive AoE rockets
- **Flamethrower** - Cone of fire with burn DoT

### Abilities (3 Types)
- **Arc Lightning** - Chain lightning damages nearby enemies
- **Ice Bullets** - Bullets slow enemy movement
- **Healing** - Enemies drop food that restores health

---

## Installation

### Requirements
- Python 3.13+
- Ursina Game Engine 8.3.0+

### Setup

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install ursina
   ```
   Or if using uv (recommended):
   ```bash
   uv sync
   ```

3. Run the game:
   ```bash
   python main.py
   ```

---

## How to Play

### Controls
- **W/A/S/D** - Move player
- **Mouse** - Look around / Aim
- **Left Click** - Fire weapon
- **ESC** - Pause / Return to menu (during gameplay)

### Game Flow

1. **Main Menu**
   - Start Game - Begin a new 5-wave session
   - Weapon Shop - Spend accumulated score to unlock weapons
   - Exit Game - Quit

2. **Gameplay**
   - Survive waves of enemies
   - Collect XP orbs (cyan) dropped by defeated enemies
   - Level up to gain abilities
   - Survive all 5 waves to win

3. **Wave Progression**
   - Wave 1: Zombies only
   - Wave 2: Zombies + Ghosts
   - Wave 3: Zombies + Ghosts + Vampires
   - Wave 4: Zombies + Ghosts + Vampires + Goblins
   - Wave 5: All enemies + Minotaur boss

4. **Ability Selection**
   - When you level up, choose from 3 random abilities at wave end
   - 60-second timer to decide
   - Abilities persist throughout the session
   - Abilities reset on new game

5. **Weapon Shop**
   - Score accumulates across all sessions (win or lose)
   - Unlock weapons with accumulated score
   - Weapon costs:
     - Shotgun: 500
     - Machine Gun: 750
     - Katana: 1000
     - Chainsaw: 1200
     - Flamethrower: 1500
     - Bazooka: 2000

---

## Project Structure

```
surviving_nightfall/
├── main.py                      # Game entry point
├── game/
│   ├── player.py                # Player controller
│   ├── camera.py                # Third-person camera
│   ├── config.py                # Game configuration
│   ├── game_manager.py          # Main game state manager
│   ├── enemies/                 # Enemy implementations
│   │   ├── base_enemy.py
│   │   ├── zombie.py
│   │   ├── ghost.py
│   │   ├── vampire.py
│   │   ├── goblin.py
│   │   └── minotaur.py
│   ├── weapons/                 # Weapon implementations
│   │   ├── base_weapon.py
│   │   ├── handgun.py
│   │   ├── shotgun.py
│   │   ├── machine_gun.py
│   │   ├── katana.py
│   │   ├── chainsaw.py
│   │   ├── bazooka.py
│   │   └── flamethrower.py
│   ├── abilities/               # Ability implementations
│   │   ├── base_ability.py
│   │   ├── arc_lightning.py
│   │   ├── ice_bullets.py
│   │   └── healing.py
│   ├── systems/                 # Game systems
│   │   ├── wave_manager.py
│   │   ├── xp_system.py
│   │   ├── score_system.py
│   │   └── collision.py
│   └── ui/                      # UI components
│       ├── main_menu.py
│       ├── hud.py
│       ├── ability_select.py
│       ├── weapon_shop.py
│       └── game_over.py
├── assets/
│   └── replacement_guide.md    # Guide for replacing 3D models
└── save_data.json              # Persistent save data (auto-generated)
```

---

## Customization

### Replacing 3D Models

Currently, the game uses basic geometric shapes (cubes, spheres) as placeholders. To replace them with your own 3D models, see the comprehensive guide:

**[Asset Replacement Guide](assets/replacement_guide.md)**

### Modifying Game Balance

Edit `game/config.py` to adjust:
- Player health and speed
- Enemy stats (HP, damage, speed)
- Weapon damage and fire rates
- XP requirements
- Wave enemy counts
- Ability parameters

Example:
```python
PLAYER_MAX_HEALTH = 150  # Increase player health
ENEMY_ZOMBIE_HP = 75     # Make zombies tougher
WEAPON_HANDGUN_DAMAGE = 30  # Increase handgun damage
```

---

## Save Data

Game progress is saved in `save_data.json` in the project root:
- Total accumulated score
- Unlocked weapons

This file persists between game sessions. Delete it to reset all progress.

---

## Development

### Adding New Enemies

1. Create a new file in `game/enemies/`
2. Inherit from `BaseEnemy`
3. Implement `ai_behavior()` and `on_death()` methods
4. Add to wave configuration in `game/config.py`
5. Import and spawn in `game/systems/wave_manager.py`

### Adding New Weapons

1. Create a new file in `game/weapons/`
2. Inherit from `BaseWeapon`
3. Implement `fire()` method
4. Add weapon cost to `game/config.py`
5. Add to weapon map in `game/game_manager.py`

### Adding New Abilities

1. Create a new file in `game/abilities/`
2. Inherit from `BaseAbility`
3. Implement required methods
4. Add to available abilities in `game/game_manager.py`

---

## Known Limitations

- Uses basic shapes as placeholders (see Asset Replacement Guide)
- No audio/sound effects (hooks provided in code comments)
- Single weapon equipped at a time
- Fixed 5-wave structure

---

## Future Enhancements

Potential features for future development:
- Sound effects and background music
- More enemy types and bosses
- Additional weapons and abilities
- Difficulty settings
- Endless mode
- Multiplayer co-op
- Procedurally generated arenas

---

## Credits

**Game Engine**: [Ursina](https://www.ursinaengine.org/)  
**Language**: Python 3.13+

---

## License

This project is provided as-is for educational and entertainment purposes.

---

## Troubleshooting

### Game won't start
- Ensure Python 3.13+ is installed
- Install Ursina: `pip install ursina`
- Check console for error messages

### Performance issues
- Lower enemy counts in `game/config.py`
- Reduce window size in `game/config.py`
- Close other applications

### Controls not working
- Ensure the game window has focus
- Check if mouse is locked (click in window)
- Verify keyboard layout

---

**Enjoy surviving the nightfall!**
