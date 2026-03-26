from ursina import Ursina, Entity, color, Sky, window, scene
from ursina.models.procedural.terrain import Terrain
from game.config import GameConfig
from game.game_manager import GameManager
from game.moon import Moon

def main():
    app = Ursina(
        title=GameConfig.WINDOW_TITLE,
        borderless=False,
        fullscreen=False,
        size=GameConfig.WINDOW_SIZE,
        vsync=True
    )
    
    
    # Create flat terrain (all height values = 0 for flat ground)
    terrain_size = 64  # Resolution of terrain grid
    flat_height_values = [[0 for _ in range(terrain_size)] for _ in range(terrain_size)]
    
    ground = Entity(
        model=Terrain(height_values=flat_height_values),
        scale=(GameConfig.GROUND_SIZE, 1, GameConfig.GROUND_SIZE),
        # color=GameConfig.GROUND_COLOR,
        texture='grass',
        collider='mesh',  # Use mesh collider for terrain
        origin_y=0
    )
    
    # ground = Entity(model='plane', collider='box', scale=64, texture='white_cube', texture_scale=(64,64))
    # Dark blue night sky
    sky = Sky(color=color.rgb32(15, 20, 40))
    sky.texture = 'sky_sunset'  # Use built-in gradient texture for better appearance
    
    # Add animated moon
    moon = Moon()
    
    game_manager = GameManager()
    
    app.run()


if __name__ == "__main__":
    main()
