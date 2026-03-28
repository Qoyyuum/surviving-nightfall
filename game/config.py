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

    ENEMY_GREEN_DEMON_HP = 50
    ENEMY_GREEN_DEMON_SPEED = 2
    ENEMY_GREEN_DEMON_DAMAGE = 10
    ENEMY_GREEN_DEMON_SIZE = Vec3(0.6, 0.6, 0.6)
    ENEMY_GREEN_DEMON_COLOR = color.rgb32(50, 150, 50)

    ENEMY_GHOST_HP = 30
    ENEMY_GHOST_SPEED = 2.5
    ENEMY_GHOST_DAMAGE = 8
    ENEMY_GHOST_SIZE = Vec3(0.6, 0.6, 0.6)
    ENEMY_GHOST_COLOR = color.rgba(200, 200, 200, 150)
    ENEMY_GHOST_DODGE_CHANCE = 0.3

    ENEMY_CYCLOPS_HP = 60
    ENEMY_CYCLOPS_SPEED = 2.2
    ENEMY_CYCLOPS_SPEED_BURST = 5.5
    ENEMY_CYCLOPS_DAMAGE = 12
    ENEMY_CYCLOPS_SIZE = Vec3(0.7, 1.6, 0.7)
    ENEMY_CYCLOPS_COLOR = color.rgb32(150, 20, 20)
    ENEMY_CYCLOPS_BURST_DURATION = 1.5
    ENEMY_CYCLOPS_BURST_COOLDOWN = 5.0

    ENEMY_BAT_HP = 25
    ENEMY_BAT_SPEED = 1.8
    ENEMY_BAT_DAMAGE = 6
    ENEMY_BAT_SIZE = Vec3(0.5, 0.8, 0.5)
    ENEMY_BAT_COLOR = color.rgb32(100, 70, 40)
    ENEMY_BAT_JUMP_COOLDOWN = 4.0
    ENEMY_BAT_JUMP_DISTANCE = 5.0

    ENEMY_CTHULHU_HP = 500
    ENEMY_CTHULHU_SPEED = 1.5
    ENEMY_CTHULHU_DAMAGE = 25
    ENEMY_CTHULHU_SIZE = Vec3(2.0, 3.0, 2.0)
    ENEMY_CTHULHU_COLOR = color.rgb32(60, 60, 60)

    # Centralized weapon data: cost, description, and stats
    WEAPONS = {
        "handgun": {
            "cost": 0,
            "description": "Starting weapon - Single shot",
            "damage": 25,
            "fire_rate": 0.3,
            "projectile_speed": 30,
            "projectile_size": 0.15,
            "projectile_color": color.yellow,
        },
        "shotgun": {
            "cost": 500,
            "description": "Fires 5 pellets in spread",
            "damage": 15,
            "fire_rate": 0.8,
            "pellets": 5,
            "spread": 15,
        },
        "machine_gun": {
            "cost": 750,
            "description": "Rapid fire, lower damage",
            "damage": 12,
            "fire_rate": 0.1,
        },
        "katana": {
            "cost": 1000,
            "description": "Dual melee blades with bleed",
            "damage": 40,
            "fire_rate": 0.4,
            "range": 2.5,
        },
        "chainsaw": {
            "cost": 1200,
            "description": "Continuous melee damage",
            "damage": 20,
            "fire_rate": 0.1,
            "range": 2.0,
        },
        "bazooka": {
            "cost": 2000,
            "description": "Explosive AoE damage",
            "damage": 150,
            "fire_rate": 2.0,
            "explosion_radius": 5.0,
        },
        "flamethrower": {
            "cost": 1500,
            "description": "Cone fire with burn DoT",
            "damage": 8,
            "fire_rate": 0.05,
            "range": 4.0,
        },
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

    WAVE_1_ENEMIES = {"green_demon": 10}
    WAVE_2_ENEMIES = {"green_demon": 10, "ghost": 5}
    WAVE_3_ENEMIES = {"green_demon": 10, "ghost": 5, "cyclops": 5}
    WAVE_4_ENEMIES = {"green_demon": 10, "ghost": 5, "cyclops": 5, "bat": 5}
    WAVE_5_ENEMIES = {
        "green_demon": 10,
        "ghost": 8,
        "cyclops": 7,
        "bat": 5,
        "cthulhu": 1,
    }

    SPAWN_RADIUS_MIN = 20
    SPAWN_RADIUS_MAX = 25
    SPAWN_STAGGER_TIME = 0.5

    XP_PER_GREEN_DEMON = 10
    XP_PER_GHOST = 15
    XP_PER_CYCLOPS = 20
    XP_PER_BAT = 12
    XP_PER_CTHULHU = 100

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

    SCORE_PER_KILL_GREEN_DEMON = 10
    SCORE_PER_KILL_GHOST = 15
    SCORE_PER_KILL_CYCLOPS = 20
    SCORE_PER_KILL_BAT = 12
    SCORE_PER_KILL_CTHULHU = 100
    SCORE_PER_WAVE = 100

    COLLISION_CHECK_INTERVAL = 0.016

    # Audio paths
    AUDIO_SFX_PATHS = {
        # Weapon sounds
        'handgun_fire': 'assets/audio/sfx/shots/pistol.wav',
        'shotgun_fire': 'assets/audio/sfx/shots/shotgun.wav',
        'machine_gun_fire': 'assets/audio/sfx/shots/cg1.wav',
        'katana_swing': 'assets/audio/sfx/katana_swing.wav',
        'chainsaw_fire': 'assets/audio/sfx/chainsaw_fire.wav',
        'bazooka_fire': 'assets/audio/sfx/bazooka_fire.wav',
        'flamethrower_fire': 'assets/audio/sfx/flamethrower_fire.wav',
        
        # Monster sounds - Green Demon
        'green_demon_spawn': 'assets/audio/sfx/green_demon_spawn.wav',
        'green_demon_attack': 'assets/audio/sfx/green_demon_attack.wav',
        'green_demon_hurt': 'assets/audio/sfx/green_demon_hurt.wav',
        'green_demon_death': 'assets/audio/sfx/green_demon_death.wav',
        
        # Monster sounds - Ghost
        'ghost_spawn': 'assets/audio/sfx/ghost_spawn.wav',
        'ghost_attack': 'assets/audio/sfx/ghost_attack.wav',
        'ghost_hurt': 'assets/audio/sfx/ghost_hurt.wav',
        'ghost_death': 'assets/audio/sfx/ghost_death.wav',
        
        # Monster sounds - Cyclops
        'cyclops_spawn': 'assets/audio/sfx/cyclops_spawn.wav',
        'cyclops_attack': 'assets/audio/sfx/cyclops_attack.wav',
        'cyclops_hurt': 'assets/audio/sfx/cyclops_hurt.wav',
        'cyclops_death': 'assets/audio/sfx/cyclops_death.wav',
        
        # Monster sounds - Bat
        'bat_spawn': 'assets/audio/sfx/bat_spawn.wav',
        'bat_attack': 'assets/audio/sfx/bat_attack.wav',
        'bat_hurt': 'assets/audio/sfx/bat_hurt.wav',
        'bat_death': 'assets/audio/sfx/bat_death.wav',
        
        # Monster sounds - Cthulhu (Boss)
        'cthulhu_spawn': 'assets/audio/sfx/cthulhu_spawn.wav',
        'cthulhu_attack': 'assets/audio/sfx/cthulhu_attack.wav',
        'cthulhu_hurt': 'assets/audio/sfx/cthulhu_hurt.wav',
        'cthulhu_death': 'assets/audio/sfx/cthulhu_death.wav',
        
        # Combat sounds
        'monster_hit': 'assets/audio/sfx/monster_hit.wav',
        'monster_death': 'assets/audio/sfx/monster_death.wav',
        'player_hit': 'assets/audio/sfx/player_hit.wav',
        'player_death': 'assets/audio/sfx/player_death.wav',
        
        # Game events
        'game_over': 'assets/audio/sfx/game_over.wav',
        'game_start': 'assets/audio/sfx/game_start.wav',
        'game_pause': 'assets/audio/sfx/game_pause.wav',
        'game_resume': 'assets/audio/sfx/game_resume.wav',
        
        # UI sounds
        'button_click': 'assets/audio/sfx/button_click.wav',
        'weapon_purchase': 'assets/audio/sfx/weapon_purchase.wav',
        
        # Ability sounds
        'arc_lightning': 'assets/audio/sfx/arc_lightning.wav',
        'healing_orb_collect': 'assets/audio/sfx/healing_orb_collect.wav',
        'xp_orb_collect': 'assets/audio/sfx/xp_orb_collect.wav',
        
        # Wave events
        'wave_complete': 'assets/audio/sfx/wave_complete.wav',
    }
    
    AUDIO_MUSIC_PATHS = {
        'menu': 'assets/audio/music/Goblins_Den_(Regular).wav',
        'battle': 'assets/audio/music/Goblins_Dance_(Battle).wav',
        'boss': 'assets/audio/music/Goblins_Dance_(Battle).wav',
    }
