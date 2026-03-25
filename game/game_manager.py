from ursina import destroy, application, mouse, camera, Vec3, Entity
from ursina.prefabs.pause_menu import PauseMenu
from game.player import Player
from game.weapons.handgun import Handgun
from game.weapons.shotgun import Shotgun
from game.weapons.machine_gun import MachineGun
from game.weapons.katana import Katana
from game.weapons.chainsaw import Chainsaw
from game.weapons.bazooka import Bazooka
from game.weapons.flamethrower import Flamethrower
from game.systems.wave_manager import WaveManager
from game.systems.xp_system import XPSystem
from game.systems.score_system import ScoreSystem
from game.systems.collision import CollisionSystem
from game.abilities.arc_lightning import ArcLightning
from game.abilities.ice_bullets import IceBullets
from game.abilities.healing import Healing
from game.ui.main_menu import MainMenu
from game.ui.hud import HUD
from game.ui.ability_select import AbilitySelectUI
from game.ui.weapon_shop import WeaponShopUI
from game.ui.game_over import GameOverUI
from game.config import GameConfig

class GameState:
    MENU = "menu"
    PLAYING = "playing"
    ABILITY_SELECT = "ability_select"
    WEAPON_SHOP = "weapon_shop"
    GAME_OVER = "game_over"

class GameManager(Entity):
    def __init__(self):
        super().__init__()
        self.eternal = True  # Don't destroy when scene.clear() is called
        self.state = GameState.MENU
        self.player = None
        self.wave_manager = None
        self.xp_system = None
        self.score_system = ScoreSystem()
        self.collision_system = CollisionSystem()
        
        self.main_menu = MainMenu(self.score_system)
        self.hud = None
        self.ability_select_ui = AbilitySelectUI()
        self.weapon_shop_ui = WeaponShopUI(self.score_system)
        self.game_over_ui = GameOverUI()
        self.pause_menu = PauseMenu()
        
        self.pending_ability_selections = []
        self.available_abilities = []
        self.next_wave_to_start = None
        
        self._setup_callbacks()
        self.show_main_menu()
        
    def _setup_callbacks(self):
        self.main_menu.on_start_game = self.start_game
        self.main_menu.on_weapon_shop = self.show_weapon_shop
        self.main_menu.on_exit_game = self.exit_game
        
        self.ability_select_ui.on_ability_selected = self.on_ability_selected
        self.ability_select_ui.on_timeout = self.on_ability_timeout
        
        self.weapon_shop_ui.on_back = self.show_main_menu
        
        self.game_over_ui.on_return_to_menu = self.return_to_menu
        
    def show_main_menu(self):
        self.cleanup_game()
        self.state = GameState.MENU
        self.main_menu.show()
        mouse.locked = False
        
    def show_weapon_shop(self):
        self.main_menu.hide()
        self.state = GameState.WEAPON_SHOP
        self.weapon_shop_ui.show()
        
    def start_game(self):
        self.main_menu.hide()
        self.weapon_shop_ui.hide()
        
        self.state = GameState.PLAYING
        mouse.locked = True
        
        self.player = Player()
        self.player.game_manager = self
        
        selected_weapon = self.score_system.unlocked_weapons[-1] if len(self.score_system.unlocked_weapons) > 0 else "handgun"
        weapon = self.create_weapon(selected_weapon)
        self.player.equip_weapon(weapon)
        
        # FirstPersonController handles camera automatically via camera_pivot
        
        self.wave_manager = WaveManager(self.player)
        self.wave_manager.on_wave_complete = self.on_wave_complete
        self.wave_manager.on_all_waves_complete = self.on_all_waves_complete
        
        self.xp_system = XPSystem(self.player)
        self.xp_system.on_level_up = self.on_level_up
        
        self.hud = HUD(self.player, self.xp_system, self.wave_manager)
        self.hud.show()
        
        self.available_abilities = [
            ArcLightning(),
            IceBullets(),
            Healing()
        ]
        
        self.score_system.reset_session()
        self.pending_ability_selections = []
        
        self.wave_manager.start_wave(1)
        
    def create_weapon(self, weapon_name):
        weapon_map = {
            "handgun": Handgun,
            "shotgun": Shotgun,
            "machine_gun": MachineGun,
            "katana": Katana,
            "chainsaw": Chainsaw,
            "bazooka": Bazooka,
            "flamethrower": Flamethrower
        }
        
        weapon_class = weapon_map.get(weapon_name, Handgun)
        return weapon_class(owner=self.player)
        
    def on_wave_complete(self, wave_number):
        # Store the next wave to start after ability selection
        self.next_wave_to_start = wave_number + 1
        
        if len(self.pending_ability_selections) > 0:
            self.show_ability_select()
        else:
            self.score_system.add_score(100)
            self.wave_manager.start_wave(self.next_wave_to_start)
            
    def on_all_waves_complete(self):
        self.end_game(victory=True)
        
    def on_level_up(self, level):
        self.pending_ability_selections.append(level)
        
    def show_ability_select(self):
        if len(self.pending_ability_selections) == 0:
            return
            
        self.state = GameState.ABILITY_SELECT
        mouse.locked = False
        
        self.pending_ability_selections.pop(0)
        
        self.ability_select_ui.show(self.available_abilities)
        
    def on_ability_selected(self, ability):
        if ability in self.player.active_abilities:
            ability.upgrade()
        else:
            self.player.add_ability(ability)
            
        if len(self.pending_ability_selections) > 0:
            self.show_ability_select()
        else:
            self.resume_game()
            
    def on_ability_timeout(self):
        if len(self.pending_ability_selections) > 0:
            self.show_ability_select()
        else:
            self.resume_game()
            
    def resume_game(self):
        self.state = GameState.PLAYING
        mouse.locked = True
        
        # Start the next wave that was queued after wave completion
        if hasattr(self, 'next_wave_to_start') and self.next_wave_to_start is not None and self.next_wave_to_start <= 5:
            self.score_system.add_score(100)
            self.wave_manager.start_wave(self.next_wave_to_start)
            self.next_wave_to_start = None  # Clear it
            
    def end_game(self, victory=False):
        self.state = GameState.GAME_OVER
        mouse.locked = False
        
        session_score = self.score_system.current_score
        self.score_system.finalize_session()
        total_score = self.score_system.total_score
        
        self.hud.hide()
        self.game_over_ui.show(victory, session_score, total_score)
        
    def return_to_menu(self):
        self.game_over_ui.hide()
        self.show_main_menu()
        
    def exit_game(self):
        application.quit()
        
    def cleanup_game(self):
        if self.player:
            destroy(self.player)
            self.player = None
            
        if self.wave_manager:
            self.wave_manager.cleanup()
            self.wave_manager = None
            
        if self.xp_system:
            self.xp_system.reset()
            self.xp_system = None
            
        if self.hud:
            self.hud.hide()
            self.hud = None
            
        for ability in self.available_abilities:
            if hasattr(ability, 'deactivate'):
                ability.deactivate()
                
        self.available_abilities = []
        
    def update(self):
        if self.state == GameState.PLAYING:
            if self.player:
                self.player.update()
            
            if self.wave_manager:
                self.wave_manager.update()
                
            if self.xp_system:
                self.xp_system.update()
                
            if self.hud:
                self.hud.update()
                
            self.handle_collisions()
            self.handle_enemy_effects()
            
            if self.player and not self.player.is_alive:
                self.end_game(victory=False)
                
        elif self.state == GameState.ABILITY_SELECT:
            if self.ability_select_ui:
                self.ability_select_ui.update()
                
    def handle_collisions(self):
        if not self.player or not self.player.current_weapon or not self.wave_manager:
            return
            
        projectiles = self.player.current_weapon.projectiles
        enemies = self.wave_manager.enemies
        
        hits = self.collision_system.check_projectile_enemy_collisions(projectiles, enemies)
        
        for hit in hits:
            self.xp_system.spawn_xp_orb(hit['position'], hit['xp'])
            self.score_system.add_score(hit['score'])
            
            healing_ability = None
            for ability in self.player.active_abilities:
                if isinstance(ability, Healing):
                    healing_ability = ability
                    break
                    
            if healing_ability:
                healing_ability.try_spawn_food(hit['position'])
                
            ice_ability = None
            for ability in self.player.active_abilities:
                if isinstance(ability, IceBullets):
                    ice_ability = ability
                    break
                    
            if ice_ability and hit['enemy']:
                ice_ability.apply_slow(hit['enemy'])
                
        xp_orbs = self.xp_system.xp_orbs
        collected_xp = self.collision_system.check_xp_collection(
            self.player, xp_orbs, self.xp_system.get_xp_required() * 0.1
        )
        
        for orb in collected_xp:
            self.xp_system.collect_orb(orb)
            
        healing_ability = None
        for ability in self.player.active_abilities:
            if isinstance(ability, Healing):
                healing_ability = ability
                break
                
        if healing_ability:
            food_orbs = healing_ability.food_orbs
            collected_food = self.collision_system.check_food_collection(
                self.player, food_orbs, 2.0
            )
            
            for orb in collected_food:
                healing_ability.collect_food(orb)
                
        if hasattr(self.player.current_weapon, 'projectiles'):
            for projectile in self.player.current_weapon.projectiles:
                if hasattr(projectile, 'explode') and projectile.age >= projectile.lifetime * 0.9:
                    projectile.explode(enemies)
                    
    def handle_enemy_effects(self):
        if not self.wave_manager:
            return
            
        for enemy in self.wave_manager.enemies:
            if not enemy or not enemy.is_alive:
                continue
                
            if hasattr(enemy, 'ice_slow_timer') and enemy.ice_slow_timer > 0:
                from ursina import time
                enemy.ice_slow_timer -= time.dt
                if enemy.ice_slow_timer <= 0:
                    enemy.speed = enemy.original_speed
                    
            if hasattr(enemy, 'bleed_timer') and enemy.bleed_timer > 0:
                from ursina import time
                enemy.bleed_timer -= time.dt
                if enemy.bleed_timer > 0 and hasattr(enemy, 'bleed_damage'):
                    enemy.take_damage(enemy.bleed_damage * time.dt)
