# Changelog

All notable changes to Surviving Nightfall will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions workflow for automated builds and releases
- Test workflow for CI/CD
- Comprehensive release guide documentation

## [1.0.0] - TBD

### Added
- Initial playable release
- 5 waves of increasing difficulty
- 7 unique weapons:
  - Handgun (starting weapon)
  - Shotgun (spread shot)
  - Machine Gun (rapid fire)
  - Katana (melee)
  - Chainsaw (continuous melee)
  - Bazooka (explosive)
  - Flamethrower (area damage)
- 3 special abilities:
  - Arc Lightning (chain damage)
  - Ice Bullets (slow enemies)
  - Healing (restore health)
- 5 enemy types:
  - Zombie (basic melee)
  - Ghost (fast, low HP)
  - Vampire (teleporting)
  - Goblin (jumping)
  - Demon (boss-like)
- Weapon shop system (unlock weapons with score)
- XP and leveling system
- Ability selection on level up
- Pause menu (ESC key)
- Hit particle effects
- Health bar UI
- Wave progression system
- Score tracking
- Game over screen

### UI Improvements
- Integrated Ursina prefabs:
  - PauseMenu for pause functionality
  - HealthBar for visual health display
  - ButtonList for weapon shop
  - ButtonGroup for ability selection
- Fixed color system (rgb → rgb32)
- Polished HUD with proper scaling

### Fixed
- Wave progression after ability selection
- Vec3.copy() errors in collision and enemy AI
- Enemy spawning and movement
- Camera controls
- Projectile-enemy collision detection

### Technical
- Built with Ursina Engine
- Python 3.13
- UV package manager
- First-person 3D gameplay
- Entity-component architecture

## Release Types

- **Major (x.0.0)**: Breaking changes, major new features
- **Minor (0.x.0)**: New features, backwards compatible  
- **Patch (0.0.x)**: Bug fixes, small improvements

## Future Plans

### v1.1.0 - Content Update
- [ ] New enemy types
- [ ] Boss wave
- [ ] More weapons
- [ ] Additional abilities

### v1.2.0 - Polish Update
- [ ] 3D models for all entities
- [ ] Textures and materials
- [ ] Sound effects
- [ ] Background music
- [ ] Better particle effects

### v2.0.0 - Major Update
- [ ] Multiple game modes
- [ ] Difficulty settings
- [ ] Save system
- [ ] Achievements
- [ ] Multiplayer (potential)
