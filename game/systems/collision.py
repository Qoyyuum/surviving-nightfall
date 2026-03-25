from ursina import distance, destroy, Vec3
from game.effects.hit_particles import create_simple_hit_effect

class CollisionSystem:
    def __init__(self):
        self.check_interval = 0.016
        self.check_timer = 0
        
    def check_projectile_enemy_collisions(self, projectiles, enemies):
        hits = []
        
        for projectile in projectiles:
            if not projectile or not projectile.enabled:
                continue
                
            for enemy in enemies:
                if not enemy or not enemy.is_alive:
                    continue
                    
                if hasattr(enemy, 'can_dodge') and enemy.can_dodge():
                    continue
                    
                dist = distance(projectile.position, enemy.position)
                
                hit_distance = 1.0
                if dist < hit_distance:
                    # Store values before enemy is potentially destroyed
                    enemy_xp = enemy.xp_value
                    enemy_score = enemy.score_value
                    enemy_pos = Vec3(enemy.position)
                    
                    # Create hit particle effect
                    create_simple_hit_effect(projectile.position)
                    
                    enemy_died = enemy.take_damage(projectile.damage)
                    destroy(projectile)
                    
                    if enemy_died:
                        hits.append({
                            'enemy': enemy,
                            'xp': enemy_xp,
                            'score': enemy_score,
                            'position': enemy_pos
                        })
                    break
                    
        return hits
        
    def check_xp_collection(self, player, xp_orbs, collection_radius):
        collected = []
        
        for orb in xp_orbs:
            if not orb or not orb.enabled:
                continue
                
            dist = distance(player.position, orb.position)
            
            if dist < collection_radius:
                collected.append(orb)
                destroy(orb)
                
        return collected
        
    def check_food_collection(self, player, food_orbs, collection_radius):
        collected = []
        
        for orb in food_orbs:
            if not orb or not orb.enabled:
                continue
                
            dist = distance(player.position, orb.position)
            
            if dist < collection_radius:
                collected.append(orb)
                destroy(orb)
                
        return collected
