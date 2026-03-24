from ursina import Vec3, color

class GameConfig:
    WINDOW_TITLE = "Surviving Nightfall"
    WINDOW_SIZE = (1280, 720)
    
    PLAYER_SPEED = 5
    PLAYER_MAX_HEALTH = 100
    PLAYER_ROTATION_SPEED = 100
    PLAYER_SIZE = Vec3(0.5, 1.8, 0.5)
    
    CAMERA_OFFSET = Vec3(0, 3, -6)
    CAMERA_ROTATION = Vec3(15, 0, 0)
    CAMERA_SMOOTHING = 0.1
    
    GROUND_SIZE = 100
    GROUND_COLOR = color.rgb32(30, 30, 40)
    
    ENEMY_ZOMBIE_HP = 50
    ENEMY_ZOMBIE_SPEED = 2
    ENEMY_ZOMBIE_DAMAGE = 10
    ENEMY_ZOMBIE_SIZE = Vec3(0.8, 1.5, 0.8)
    ENEMY_ZOMBIE_COLOR = color.rgb32(50, 150, 50)
    
    ENEMY_GHOST_HP = 30
    ENEMY_GHOST_SPEED = 2.5
    ENEMY_GHOST_DAMAGE = 8
    ENEMY_GHOST_SIZE = 0.7
    ENEMY_GHOST_COLOR = color.rgba(200, 200, 200, 150)
    ENEMY_GHOST_DODGE_CHANCE = 0.3
    
    ENEMY_VAMPIRE_HP = 60
    ENEMY_VAMPIRE_SPEED = 2.2
    ENEMY_VAMPIRE_SPEED_BURST = 5.5
    ENEMY_VAMPIRE_DAMAGE = 12
    ENEMY_VAMPIRE_SIZE = Vec3(0.7, 1.6, 0.7)
    ENEMY_VAMPIRE_COLOR = color.rgb32(150, 20, 20)
    ENEMY_VAMPIRE_BURST_DURATION = 1.5
    ENEMY_VAMPIRE_BURST_COOLDOWN = 5.0
    
    ENEMY_GOBLIN_HP = 25
    ENEMY_GOBLIN_SPEED = 1.8
    ENEMY_GOBLIN_DAMAGE = 6
    ENEMY_GOBLIN_SIZE = Vec3(0.5, 0.8, 0.5)
    ENEMY_GOBLIN_COLOR = color.rgb32(100, 70, 40)
    ENEMY_GOBLIN_JUMP_COOLDOWN = 4.0
    ENEMY_GOBLIN_JUMP_DISTANCE = 5.0
    
    ENEMY_MINOTAUR_HP = 500
    ENEMY_MINOTAUR_SPEED = 1.5
    ENEMY_MINOTAUR_DAMAGE = 25
    ENEMY_MINOTAUR_SIZE = Vec3(2.0, 3.0, 2.0)
    ENEMY_MINOTAUR_COLOR = color.rgb32(60, 60, 60)
    
    # Centralized weapon data: cost, description, and stats
    WEAPONS = {
        "handgun": {
            "cost": 0,
            "description": "Starting weapon - Single shot",
            "damage": 25,
            "fire_rate": 0.3,
            "projectile_speed": 30,
            "projectile_size": 0.15,
            "projectile_color": color.yellow
        },
        "shotgun": {
            "cost": 500,
            "description": "Fires 5 pellets in spread",
            "damage": 15,
            "fire_rate": 0.8,
            "pellets": 5,
            "spread": 15
        },
        "machine_gun": {
            "cost": 750,
            "description": "Rapid fire, lower damage",
            "damage": 12,
            "fire_rate": 0.1
        },
        "katana": {
            "cost": 1000,
            "description": "Dual melee blades with bleed",
            "damage": 40,
            "fire_rate": 0.4,
            "range": 2.5
        },
        "chainsaw": {
            "cost": 1200,
            "description": "Continuous melee damage",
            "damage": 20,
            "fire_rate": 0.1,
            "range": 2.0
        },
        "bazooka": {
            "cost": 2000,
            "description": "Explosive AoE damage",
            "damage": 150,
            "fire_rate": 2.0,
            "explosion_radius": 5.0
        },
        "flamethrower": {
            "cost": 1500,
            "description": "Cone fire with burn DoT",
            "damage": 8,
            "fire_rate": 0.05,
            "range": 4.0
        }
    }
    
    # Legacy constants for backward compatibility (can be removed later)
    WEAPON_HANDGUN_DAMAGE = 25
    WEAPON_HANDGUN_FIRE_RATE = 0.3
    WEAPON_HANDGUN_PROJECTILE_SPEED = 30
    WEAPON_HANDGUN_PROJECTILE_SIZE = 0.15
    WEAPON_HANDGUN_PROJECTILE_COLOR = color.yellow
    
    WEAPON_SHOTGUN_DAMAGE = 15
    WEAPON_SHOTGUN_FIRE_RATE = 0.8
    WEAPON_SHOTGUN_PELLETS = 5
    WEAPON_SHOTGUN_SPREAD = 15
    WEAPON_SHOTGUN_COST = 500
    
    WEAPON_MACHINEGUN_DAMAGE = 12
    WEAPON_MACHINEGUN_FIRE_RATE = 0.1
    WEAPON_MACHINEGUN_COST = 750
    
    WEAPON_KATANA_DAMAGE = 40
    WEAPON_KATANA_FIRE_RATE = 0.4
    WEAPON_KATANA_RANGE = 2.5
    WEAPON_KATANA_COST = 1000
    
    WEAPON_CHAINSAW_DAMAGE = 20
    WEAPON_CHAINSAW_FIRE_RATE = 0.1
    WEAPON_CHAINSAW_RANGE = 2.0
    WEAPON_CHAINSAW_COST = 1200
    
    WEAPON_BAZOOKA_DAMAGE = 150
    WEAPON_BAZOOKA_FIRE_RATE = 2.0
    WEAPON_BAZOOKA_EXPLOSION_RADIUS = 5.0
    WEAPON_BAZOOKA_COST = 2000
    
    WEAPON_FLAMETHROWER_DAMAGE = 8
    WEAPON_FLAMETHROWER_FIRE_RATE = 0.05
    WEAPON_FLAMETHROWER_RANGE = 4.0
    WEAPON_FLAMETHROWER_COST = 1500
    
    PROJECTILE_LIFETIME = 3.0
    
    WAVE_1_ENEMIES = {"zombie": 10}
    WAVE_2_ENEMIES = {"zombie": 10, "ghost": 5}
    WAVE_3_ENEMIES = {"zombie": 10, "ghost": 5, "vampire": 5}
    WAVE_4_ENEMIES = {"zombie": 10, "ghost": 5, "vampire": 5, "goblin": 5}
    WAVE_5_ENEMIES = {"zombie": 10, "ghost": 8, "vampire": 7, "goblin": 5, "minotaur": 1}
    
    SPAWN_RADIUS_MIN = 20
    SPAWN_RADIUS_MAX = 25
    SPAWN_STAGGER_TIME = 0.5
    
    XP_PER_ZOMBIE = 10
    XP_PER_GHOST = 15
    XP_PER_VAMPIRE = 20
    XP_PER_GOBLIN = 12
    XP_PER_MINOTAUR = 100
    
    XP_LEVEL_BASE = 100
    XP_LEVEL_MULTIPLIER = 1.5
    
    XP_ORB_SIZE = 0.3
    XP_ORB_COLOR = color.cyan
    XP_COLLECTION_RADIUS = 2.0
    
    ABILITY_SELECT_TIMEOUT = 60.0
    
    ABILITY_ARC_LIGHTNING_DAMAGE = 30
    ABILITY_ARC_LIGHTNING_TARGETS = 3
    ABILITY_ARC_LIGHTNING_RANGE = 8.0
    ABILITY_ARC_LIGHTNING_COOLDOWN = 5.0
    
    ABILITY_ICE_BULLETS_SLOW = 0.5
    ABILITY_ICE_BULLETS_DURATION = 2.0
    
    ABILITY_HEALING_AMOUNT = 15
    ABILITY_HEALING_DROP_CHANCE = 0.2
    
    FOOD_ORB_SIZE = 0.25
    FOOD_ORB_COLOR = color.pink
    
    SCORE_PER_KILL_ZOMBIE = 10
    SCORE_PER_KILL_GHOST = 15
    SCORE_PER_KILL_VAMPIRE = 20
    SCORE_PER_KILL_GOBLIN = 12
    SCORE_PER_KILL_MINOTAUR = 100
    SCORE_PER_WAVE = 100
    
    COLLISION_CHECK_INTERVAL = 0.016
