# Weapon Visual Guide

The game now uses **First Person Controller** with visible weapon models in your view.

## Current Weapon Visuals

Each weapon has a distinct color and size to help identify it:

| Weapon | Color | Size | Visual Description |
|--------|-------|------|-------------------|
| **Handgun** | Gray | Small | Compact pistol shape |
| **Shotgun** | Brown | Medium-Large | Wide, chunky barrel |
| **Machine Gun** | Black | Medium | Sleek automatic weapon |
| **Katana** | Cyan | Long & Thin | Sword extending forward |
| **Chainsaw** | Orange | Chunky | Square, mechanical look |
| **Bazooka** | Olive | Large | Big tube launcher |
| **Flamethrower** | Red | Medium-Large | Fuel tank appearance |

## Weapon Position

Weapons appear in the **bottom right** of your screen:
- Position: `(0.4, -0.3, 0.5)` relative to camera
- Slight downward tilt for natural look
- Parented to camera so it moves with your view

## Replacing with Custom Models

To replace placeholder cubes with actual 3D models:

### Step 1: Prepare Your Model
- Export as `.obj`, `.bam`, or `.glb`
- Place in `assets/models/weapons/`
- Example: `assets/models/weapons/handgun.obj`

### Step 2: Update Player Code

Edit `game/player.py` in the `equip_weapon` method:

```python
weapon_visuals = {
    "Handgun": {
        "model": "assets/models/weapons/handgun.obj",  # Change from "cube"
        "color": color.white,  # Use white for textured models
        "scale": (1, 1, 1),    # Adjust scale as needed
        "position": (0.4, -0.3, 0.5),
        "rotation": (-10, 0, 0)
    },
    # ... other weapons
}
```

### Step 3: Adjust Position/Scale

Each weapon may need different positioning:

```python
self.weapon_model = Entity(
    parent=camera,
    model=visual["model"],
    texture=visual.get("texture"),  # Optional texture
    color=visual["color"],
    scale=visual["scale"],
    position=visual.get("position", (0.4, -0.3, 0.5)),
    rotation=visual.get("rotation", (-10, 0, 0))
)
```

## Camera System

The game now uses Ursina's built-in `FirstPersonController`:
- ✅ Automatic camera following
- ✅ Mouse look controls
- ✅ Smooth movement
- ✅ Built-in collision detection
- ✅ Jump capability (Space key)

### Controls
- **WASD** - Move
- **Mouse** - Look around
- **Left Click** - Fire weapon
- **Space** - Jump
- **ESC** - Pause/Menu

## Technical Details

### Camera Hierarchy
```
Player (FirstPersonController)
  └─ camera_pivot (Entity at player height)
      └─ camera
          └─ weapon_model (visible in view)
```

The `camera_pivot` is automatically created by `FirstPersonController` and handles:
- Vertical rotation (pitch)
- Smooth camera movement
- Proper parent-child relationships

### Why This Works Better

**Old System (ThirdPersonCamera):**
- Manual position calculation every frame
- Lerp smoothing caused lag
- Camera position set by menus interfered

**New System (FirstPersonController):**
- Parent-child hierarchy (camera → camera_pivot → player)
- Automatic updates via Ursina's Entity system
- No manual position calculations needed
- Weapon models parent to camera for perfect alignment

---

**Ready to add your weapon models!** 🎮
