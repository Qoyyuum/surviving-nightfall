# Quick Start Guide - Surviving Nightfall

## Running the Game

Since this project uses `uv` for dependency management:

```bash
# Run the game
uv run python main.py
```

## First Time Setup

The dependencies are already configured in `pyproject.toml`. Just run:

```bash
uv sync
```

This will install Ursina and all required dependencies.

## Controls

- **WASD** - Move
- **Mouse** - Look/Aim
- **Left Click** - Shoot
- **ESC** - Exit to menu

## Game Flow

1. **Main Menu** appears on launch
   - Click "Start Game" to begin
   - Click "Weapon Shop" to unlock weapons with accumulated score
   - Click "Exit Game" to quit

2. **Survive 5 Waves**
   - Wave 1: Green Demons only
   - Wave 2: Green Demons + Ghosts
   - Wave 3: Green Demons + Ghosts + Cyclops
   - Wave 4: All above + Bats
   - Wave 5: All enemies + Cthulhu boss

3. **Level Up Between Waves**
   - Collect cyan XP orbs from defeated enemies
   - Choose abilities when you level up
   - 60 seconds to select or it carries to next wave

4. **Unlock Weapons**
   - Score persists across all sessions
   - Use accumulated score in Weapon Shop
   - Unlocked weapons stay unlocked forever

## Tips

- Keep moving to avoid being surrounded
- Collect XP orbs quickly before they despawn
- Choose abilities that complement your playstyle
- Save score for expensive weapons (Bazooka costs 2000!)

## Troubleshooting

**Game won't start:**
```bash
uv sync
uv run python main.py
```

**Performance issues:**
Edit `game/config.py` and reduce enemy counts or window size.

**Want to reset progress:**
Delete `save_data.json` in the project root.

---

**Have fun surviving the nightfall!**
