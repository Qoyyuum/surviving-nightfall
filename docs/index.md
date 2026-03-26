# Surviving Nightfall Documentation

Welcome to the documentation for **Surviving Nightfall**, a 3D third-person bullet hell survival game.

## Documentation Index

### Getting Started
- **[README](README.md)** - Complete game documentation and features
- **[Quick Start Guide](QUICKSTART.md)** - Installation and running the game

### Development Guides
- **[Weapon Configuration Guide](WEAPON_CONFIG_GUIDE.md)** - How to add and modify weapons
- **[Asset Replacement Guide](replacement_guide.md)** - Replace 3D models and textures

## Game Overview

**Surviving Nightfall** is a roguelike permadeath survival game where you fight through waves of supernatural enemies. Armed with various weapons and special abilities, survive 5 increasingly difficult waves to claim victory.

### Key Features

- **5 Wave Progression** - Each wave introduces new enemy types
- **7 Weapons** - From handgun to bazooka, each with unique mechanics
- **3 Special Abilities** - Arc Lightning, Ice Bullets, and Healing
- **Persistent Progression** - Unlock weapons permanently with accumulated score
- **Roguelike Elements** - Permadeath with persistent weapon unlocks

### Enemy Types

1. **Green Demon** - Basic melee attacker
2. **Ghost** - Can dodge bullets (30% chance)
3. **Cyclops** - Speed burst ability
4. **Bat** - Jump attacks
5. **Cthulhu** - High HP boss (Wave 5 only)

### Weapons

| Weapon | Cost | Type | Description |
|--------|------|------|-------------|
| Handgun | 0 | Ranged | Starting weapon |
| Shotgun | 500 | Ranged | Spread fire |
| Machine Gun | 750 | Ranged | Rapid fire |
| Katana | 1000 | Melee | Bleed damage |
| Chainsaw | 1200 | Melee | Continuous damage |
| Flamethrower | 1500 | Ranged | Fire DoT |
| Bazooka | 2000 | Ranged | Explosive AoE |

## Project Structure

```
surviving_nightfall/
├── main.py                  # Game entry point
├── game/
│   ├── config.py           # Centralized game configuration
│   ├── player.py           # Player controller
│   ├── camera.py           # Third-person camera
│   ├── game_manager.py     # Game state manager
│   ├── enemies/            # Enemy implementations
│   ├── weapons/            # Weapon implementations
│   ├── abilities/          # Ability implementations
│   ├── systems/            # Game systems (waves, XP, score, collision)
│   └── ui/                 # UI components
├── assets/                 # Game assets (models, textures)
└── docs/                   # Documentation
```

## Contributing

When adding new features:

1. Follow the existing code structure
2. Add configuration to `game/config.py`
3. Update relevant documentation
4. Test thoroughly before committing

## Support

For issues or questions:
- Check the documentation guides
- Review the code comments
- Examine existing implementations as examples

---

**Happy coding and surviving!**
