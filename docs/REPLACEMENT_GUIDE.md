# Asset Replacement Guide - Surviving Nightfall

This guide explains how to replace the basic geometric shapes (cubes, spheres, etc.) with your own 3D models in the Surviving Nightfall game.

---

## Table of Contents

1. [Overview](#overview)
2. [Supported File Formats](#supported-file-formats)
3. [Asset Organization](#asset-organization)
4. [Replacing Player Model](#replacing-player-model)
5. [Replacing Enemy Models](#replacing-enemy-models)
6. [Replacing Projectiles](#replacing-projectiles)
7. [Replacing Collectibles](#replacing-collectibles)
8. [Adding Textures](#adding-textures)
9. [Scaling and Positioning](#scaling-and-positioning)
10. [Animation Support](#animation-support)

---

## Overview

Currently, all game objects use basic Ursina primitives:
- **Player**: White capsule/cube
- **Enemies**: Colored cubes and spheres
- **Projectiles**: Small colored spheres
- **Collectibles**: Small spheres (XP = cyan, Food = pink)

You can replace these with your own 3D models by modifying the `model` parameter in the respective class files.

---

## Supported File Formats

Ursina supports the following 3D model formats:
- **.obj** (Recommended - widely supported, simple)
- **.glb** / **.gltf** (Good for animations)
- **.bam** (Panda3D native format - best performance)
- **.blend** (Blender files - requires Blender installed)

**Recommendation**: Use `.obj` files for static models and `.glb` for animated models.

---

## Asset Organization

Create the following folder structure in your project:

```
surviving_nightfall/
├── assets/
│   ├── models/
│   │   ├── player/
│   │   │   └── player_character.obj
│   │   ├── enemies/
│   │   │   ├── zombie.obj
│   │   │   ├── ghost.obj
│   │   │   ├── vampire.obj
│   │   │   ├── goblin.obj
│   │   │   └── minotaur.obj
│   │   ├── weapons/
│   │   │   └── (weapon models if needed)
│   │   └── collectibles/
│   │       ├── xp_orb.obj
│   │       └── food_orb.obj
│   ├── textures/
│   │   ├── player_texture.png
│   │   ├── zombie_texture.png
│   │   └── (other textures)
│   └── replacement_guide.md (this file)
```

---

## Replacing Player Model

### Location
File: `game/player.py`

### Current Code
```python
super().__init__(
    model='cube',
    color=color.white,
    scale=GameConfig.PLAYER_SIZE,
    # ...
)
```

### Replacement Example
```python
super().__init__(
    model='assets/models/player/player_character.obj',
    texture='assets/textures/player_texture.png',  # Optional
    scale=1,  # Adjust as needed
    # ...
)
```

### Tips
- The player model should face forward along the **positive Z-axis**
- Recommended height: 1.5-2.0 units
- Center the model at origin (0, 0, 0) in your 3D software
- If the model appears too large/small, adjust the `scale` parameter

---

## Replacing Enemy Models

### Zombie

**File**: `game/enemies/zombie.py`

**Current**:
```python
super().__init__(
    model='cube',
    # ...
)
```

**Replacement**:
```python
super().__init__(
    model='assets/models/enemies/zombie.obj',
    texture='assets/textures/zombie_texture.png',
    # ...
)
```

### Ghost

**File**: `game/enemies/ghost.py`

**Current**:
```python
super().__init__(
    model='sphere',
    # ...
)
```

**Replacement**:
```python
super().__init__(
    model='assets/models/enemies/ghost.obj',
    texture='assets/textures/ghost_texture.png',
    alpha=0.6,  # For transparency effect
    # ...
)
```

**Note**: For ghosts, you may want to use a semi-transparent texture or material.

### Vampire

**File**: `game/enemies/vampire.py`

**Replacement**: Same pattern as Zombie

### Goblin

**File**: `game/enemies/goblin.py`

**Note**: Goblins are smaller enemies. Make sure your model is appropriately scaled (about 0.5-0.8 units tall).

### Minotaur

**File**: `game/enemies/minotaur.py`

**Note**: Minotaurs are large boss enemies. Scale should be 2-3x larger than normal enemies.

---

## Replacing Projectiles

### Bullet Projectiles

**File**: `game/weapons/base_weapon.py`

**Current** (in Projectile class):
```python
super().__init__(
    model='sphere',
    scale=size,
    color=color,
    # ...
)
```

**Replacement**:
```python
super().__init__(
    model='assets/models/projectiles/bullet.obj',
    scale=size,
    texture='assets/textures/bullet_texture.png',
    # ...
)
```

### Weapon-Specific Projectiles

Different weapons can use different projectile models:
- **Handgun/Machine Gun**: Small bullet model
- **Shotgun**: Pellet model (smaller)
- **Bazooka**: Rocket model (larger, with fins)
- **Flamethrower**: Flame particle model

Modify the respective weapon files (`handgun.py`, `shotgun.py`, etc.) to use different models.

---

## Replacing Collectibles

### XP Orbs

**File**: `game/systems/xp_system.py` (XPOrb class)

**Current**:
```python
super().__init__(
    model='sphere',
    scale=GameConfig.XP_ORB_SIZE,
    color=GameConfig.XP_ORB_COLOR,
    # ...
)
```

**Replacement**:
```python
super().__init__(
    model='assets/models/collectibles/xp_orb.obj',
    scale=GameConfig.XP_ORB_SIZE,
    texture='assets/textures/xp_orb_glow.png',
    # ...
)
```

### Food Orbs

**File**: `game/abilities/healing.py` (FoodOrb class)

**Replacement**: Same pattern as XP Orbs

---

## Adding Textures

### Basic Texture Application

```python
Entity(
    model='assets/models/player.obj',
    texture='assets/textures/player_diffuse.png'
)
```

### Multiple Textures (Advanced)

For models with multiple materials:

```python
from ursina import load_texture

player = Entity(
    model='assets/models/player.obj'
)
player.texture = load_texture('assets/textures/player_diffuse.png')
```

### Texture Formats
- **.png** (Recommended - supports transparency)
- **.jpg** (Good for non-transparent textures)
- **.tga** (Supports alpha channel)

---

## Scaling and Positioning

### Finding the Right Scale

1. Load your model with `scale=1`
2. Run the game and observe the size
3. Adjust the scale value:
   - Too large? Decrease scale (e.g., `scale=0.5`)
   - Too small? Increase scale (e.g., `scale=2`)

### Adjusting Position Offset

If your model appears offset from where it should be:

```python
self.position += Vec3(0, -0.5, 0)  # Move down by 0.5 units
```

### Rotation

If your model faces the wrong direction:

```python
self.rotation_y = 180  # Rotate 180 degrees
```

---

## Animation Support

### Adding Animations (Advanced)

For animated models (`.glb` format recommended):

**Example - Animated Player**:

```python
from ursina import Animation

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='assets/models/player/player_animated.glb',
            # ...
        )
        
        # Load animations
        self.animator = Animation('assets/models/player/player_animated.glb')
        
        # Play idle animation
        self.animator.play('idle')
        
    def update(self):
        # Switch to walk animation when moving
        if self.is_moving:
            self.animator.play('walk')
        else:
            self.animator.play('idle')
```

### Animation Naming Conventions

Common animation names in your 3D software:
- `idle` - Standing still
- `walk` - Walking movement
- `run` - Running movement
- `attack` - Attack animation
- `death` - Death animation
- `hit` - Taking damage

---

## Quick Reference Table

| Object Type | File Location | Current Model | Recommended Size |
|-------------|---------------|---------------|------------------|
| Player | `game/player.py` | `'cube'` | 1.5-2.0 units tall |
| Zombie | `game/enemies/zombie.py` | `'cube'` | 1.5 units tall |
| Ghost | `game/enemies/ghost.py` | `'sphere'` | 0.7 units radius |
| Vampire | `game/enemies/vampire.py` | `'cube'` | 1.6 units tall |
| Goblin | `game/enemies/goblin.py` | `'cube'` | 0.8 units tall |
| Minotaur | `game/enemies/minotaur.py` | `'cube'` | 3.0 units tall |
| Bullet | `game/weapons/base_weapon.py` | `'sphere'` | 0.15 units |
| XP Orb | `game/systems/xp_system.py` | `'sphere'` | 0.3 units |
| Food Orb | `game/abilities/healing.py` | `'sphere'` | 0.25 units |

---

## Testing Your Models

1. Replace one model at a time
2. Run the game: `python main.py`
3. Check for:
   - Correct size and scale
   - Proper orientation (facing forward)
   - Textures loading correctly
   - No performance issues

---

## Troubleshooting

### Model doesn't appear
- Check file path is correct
- Ensure model file exists in the specified location
- Try using absolute path: `model=r'C:\full\path\to\model.obj'`

### Model is too large/small
- Adjust the `scale` parameter
- Or re-export the model at a different scale in your 3D software

### Model faces wrong direction
- Rotate in code: `self.rotation_y = 180`
- Or re-orient in your 3D software before exporting

### Texture doesn't load
- Ensure texture path is correct
- Check texture file format (use .png or .jpg)
- Verify texture is in the same folder or use full path

### Performance issues
- Reduce polygon count in your 3D models
- Use smaller texture sizes (512x512 or 1024x1024)
- Convert models to .bam format for better performance

---

## Example: Complete Player Replacement

Here's a complete example of replacing the player model:

**File**: `game/player.py`

```python
# Original
super().__init__(
    model='cube',
    color=color.white,
    scale=GameConfig.PLAYER_SIZE,
    position=(0, GameConfig.PLAYER_SIZE.y / 2, 0),
    collider='box',
    **kwargs
)

# Replaced with custom model
super().__init__(
    model='assets/models/player/survivor.obj',
    texture='assets/textures/player/survivor_diffuse.png',
    scale=1.5,  # Adjust based on your model
    position=(0, 0, 0),  # Model should be centered at origin
    collider='box',
    **kwargs
)
```

---

## Additional Resources

- **Ursina Documentation**: https://www.ursinaengine.org/documentation.html
- **Free 3D Models**: 
  - Mixamo (animated characters)
  - Sketchfab (various models)
  - OpenGameArt.org
- **3D Software**:
  - Blender (free, open-source)
  - Maya, 3ds Max (professional)

---

## Need Help?

If you encounter issues:
1. Check the Ursina documentation
2. Verify your model loads in Blender or another 3D viewer
3. Test with a simple .obj cube first to ensure the pipeline works
4. Check console output for error messages

---

**Happy Modding!**
