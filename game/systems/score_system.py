import json
import os
from game.config import GameConfig

class ScoreSystem:
    def __init__(self, save_file="save_data.json"):
        self.save_file = save_file
        self.current_score = 0
        self.total_score = 0
        self.unlocked_weapons = ["handgun"]
        
        # Build weapon_costs from centralized WEAPONS config
        self.weapon_costs = {
            weapon_name: weapon_data["cost"]
            for weapon_name, weapon_data in GameConfig.WEAPONS.items()
        }
        
        self.load_data()
        
    def add_score(self, amount):
        self.current_score += amount
        
    def finalize_session(self):
        self.total_score += self.current_score
        self.save_data()
        
    def reset_session(self):
        self.current_score = 0
        
    def can_afford(self, weapon_name):
        if weapon_name not in self.weapon_costs:
            return False
        return self.total_score >= self.weapon_costs[weapon_name]
        
    def is_unlocked(self, weapon_name):
        return weapon_name in self.unlocked_weapons
        
    def unlock_weapon(self, weapon_name):
        if weapon_name in self.unlocked_weapons:
            return False
            
        if not self.can_afford(weapon_name):
            return False
            
        cost = self.weapon_costs[weapon_name]
        self.total_score -= cost
        self.unlocked_weapons.append(weapon_name)
        self.save_data()
        return True
        
    def save_data(self):
        data = {
            "total_score": self.total_score,
            "unlocked_weapons": self.unlocked_weapons
        }
        
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Failed to save data: {e}")
            
    def load_data(self):
        if not os.path.exists(self.save_file):
            return
            
        try:
            with open(self.save_file, 'r') as f:
                data = json.load(f)
                
            self.total_score = data.get("total_score", 0)
            self.unlocked_weapons = data.get("unlocked_weapons", ["handgun"])
        except Exception as e:
            print(f"Failed to load data: {e}")
