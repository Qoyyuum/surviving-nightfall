from ursina import Ursina, Entity, color, Sky, window
from ursina.models.procedural.terrain import Terrain
from game.config import GameConfig
from game.game_manager import GameManager

def main():
    app = Ursina(
        title=GameConfig.WINDOW_TITLE,
        borderless=False,
        fullscreen=False,
        size=GameConfig.WINDOW_SIZE,
        vsync=True
    )
    
    window.color = color.rgb32(10, 10, 20)
    
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
    
    # Dark blue night sky
    # sky = Sky(color=color.rgb32(15, 20, 40))
    # sky.texture = 'sky_sunset'  # Use built-in gradient texture for better appearance
    sky = Sky(texture="sky_night")
    sky.ground = ground
    
    game_manager = GameManager()
    
    app.run()


if __name__ == "__main__":
    main()
