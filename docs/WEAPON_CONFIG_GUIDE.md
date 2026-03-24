# Weapon Configuration Guide

All weapon data is now centralized in `game/config.py` under the `WEAPONS` dictionary for easy maintenance and extension.

## Location

**File**: `game/config.py`  
**Variable**: `GameConfig.WEAPONS`

## Structure

```python
WEAPONS = {
    "weapon_name": {
        "cost": 0,                    # Score cost to unlock
        "description": "...",         # Description shown in shop
        "damage": 25,                 # Base damage
        "fire_rate": 0.3,            # Seconds between shots
        # ... weapon-specific stats
    }
}
```

## Current Weapons

| Weapon | Cost | Description |
|--------|------|-------------|
| Handgun | 0 | Starting weapon - Single shot |
| Shotgun | 500 | Fires 5 pellets in spread |
| Machine Gun | 750 | Rapid fire, lower damage |
| Katana | 1000 | Dual melee blades with bleed |
| Chainsaw | 1200 | Continuous melee damage |
| Bazooka | 2000 | Explosive AoE damage |
| Flamethrower | 1500 | Cone fire with burn DoT |

## How to Add a New Weapon

### Step 1: Add to GameConfig.WEAPONS

Edit `game/config.py`:

```python
WEAPONS = {
    # ... existing weapons ...
    
    "sniper_rifle": {
        "cost": 1800,
        "description": "High damage, slow fire rate",
        "damage": 200,
        "fire_rate": 2.0,
        "projectile_speed": 50,
        "projectile_size": 0.2
    }
}
```

### Step 2: Create Weapon Class

Create `game/weapons/sniper_rifle.py`:

```python
from game.weapons.base_weapon import BaseWeapon, Projectile
from game.config import GameConfig
from ursina import color

class SniperRifle(BaseWeapon):
    def __init__(self, owner=None):
        weapon_data = GameConfig.WEAPONS["sniper_rifle"]
        super().__init__(
            name="Sniper Rifle",
            damage=weapon_data["damage"],
            fire_rate=weapon_data["fire_rate"],
            owner=owner
        )
        self.projectile_speed = weapon_data["projectile_speed"]
        self.projectile_size = weapon_data["projectile_size"]
        
    def fire(self):
        if not self.owner:
            return
            
        projectile = Projectile(
            position=self.owner.position + (0, 1, 0),
            direction=self.owner.forward,
            speed=self.projectile_speed,
            damage=self.damage,
            lifetime=5.0,
            size=self.projectile_size,
            color=color.orange,
            owner=self.owner
        )
        self.projectiles.append(projectile)
```

### Step 3: Register in GameManager

Edit `game/game_manager.py`, add to weapon map:

```python
self.weapon_map = {
    "handgun": Handgun,
    "shotgun": Shotgun,
    "machine_gun": MachineGun,
    "katana": Katana,
    "chainsaw": Chainsaw,
    "bazooka": Bazooka,
    "flamethrower": Flamethrower,
    "sniper_rifle": SniperRifle  # Add this line
}
```

And import at the top:

```python
from game.weapons.sniper_rifle import SniperRifle
```

### Step 4: Done!

The weapon will automatically appear in:
- ✅ Weapon shop UI (with cost and description)
- ✅ Score system (unlock tracking)
- ✅ Save/load system (persistence)

## How to Modify Existing Weapons

Just edit the values in `GameConfig.WEAPONS`:

```python
"shotgun": {
    "cost": 500,           # Change to 400 to make cheaper
    "description": "...",
    "damage": 15,          # Change to 20 for more damage
    "fire_rate": 0.8,      # Change to 0.6 for faster fire
    "pellets": 5,          # Change to 7 for more pellets
    "spread": 15
}
```

Changes take effect immediately on next game run.

## Systems That Use This Config

1. **ScoreSystem** (`game/systems/score_system.py`)
   - Reads `cost` for each weapon
   - Builds `weapon_costs` dictionary automatically

2. **WeaponShopUI** (`game/ui/weapon_shop.py`)
   - Reads `description` for display
   - Reads `cost` for pricing
   - Iterates through all weapons automatically

3. **Weapon Classes** (individual weapon files)
   - Can read their own stats from `GameConfig.WEAPONS[weapon_name]`
   - Use stats for damage, fire rate, etc.

## Benefits

✅ **Single source of truth** - All weapon data in one place  
✅ **Easy to extend** - Add new weapons by editing one file  
✅ **Easy to balance** - Tweak costs and stats in one location  
✅ **Automatic UI updates** - Shop displays all weapons automatically  
✅ **Type-safe** - All weapons follow the same structure  

## Legacy Constants

The old individual constants (e.g., `WEAPON_SHOTGUN_COST`) are kept for backward compatibility but can be removed once all weapon classes are updated to use the new `WEAPONS` dictionary.

---

**Happy weapon crafting!**
