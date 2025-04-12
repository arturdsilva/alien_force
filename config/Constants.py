class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    LIGHT_PURPLE = (180, 120, 200)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (200, 200, 200)
    BROWN = (139, 69, 19)
    PINK = (255, 192, 203)


class Constants:
    # GENERAL
    FPS = 60
    WIDTH = 800
    HEIGHT = 600
    GRAVITY = 3000
    EPSILON = 1.0e-9
    BACKGROUND_COLOR = Colors.LIGHT_PURPLE
    TERRAIN_COLOR = Colors.BLACK

    # DIFFICULTY
    SPEED_MULTIPLIER_LIMIT = 2.0
    TIME_UNTIL_LIMIT_DIFFICULTY = 120.0
    DIFFICULTY_FACTOR = (SPEED_MULTIPLIER_LIMIT - 1.0) / (
            TIME_UNTIL_LIMIT_DIFFICULTY * FPS)

    # PLAYER
    PLAYER_WIDTH = 50
    PLAYER_HEIGHT = 100
    PLAYER_SPEED = 100
    PLAYER_DEFAULT_COLOR = Colors.DARK_GRAY
    JUMP_SPEED = 700
    PLAYER_MAX_HEALTH = 100

    # ENEMIES
    MAX_ENEMIES = 20
    ENEMY_SPEED = 100
    SPAWN_TIMER = 2.5

    # Wavy Enemy
    WAVY_ENEMY_WIDTH = 50
    WAVY_ENEMY_HEIGHT = 30
    WAVY_ENEMY_Y = 100
    WAVY_ENEMY_AMPLITUDE = 100
    WAVY_ENEMY_ANGULAR_FREQUENCY = 3
    WAVY_ENEMY_MAX_HEALTH = 100
    WAVY_ENEMY_SPEED = 1.0 * ENEMY_SPEED

    # Linear Enemy
    LINEAR_ENEMY_WIDTH = 40
    LINEAR_ENEMY_HEIGHT = 40
    LINEAR_ENEMY_MAX_HEALTH = 80
    LINEAR_ENEMY_SPEED = 150

    # Bouncing Enemy
    BOUNCING_ENEMY_WIDTH = 35
    BOUNCING_ENEMY_HEIGHT = 35
    BOUNCING_ENEMY_MAX_HEALTH = 60
    BOUNCING_ENEMY_HORIZONTAL_SPEED = 150
    BOUNCING_ENEMY_FALL_SPEED = 500
    BOUNCING_ENEMY_RISE_SPEED = 100
    BOUNCING_ENEMY_BASE_HEIGHT = HEIGHT / 4  # Altura base para movimento horizontal
    BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL = 2  # Tempo mínimo antes de cair
    BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL = 5  # Tempo máximo antes de cair
    BOUNCING_ENEMY_WAIT_TIME = 1  # Tempo de espera após cair/subir

    # Tank Enemy
    TANK_ENEMY_WIDTH = 80
    TANK_ENEMY_HEIGHT = 60
    TANK_ENEMY_MAX_HEALTH = 200
    TANK_ENEMY_SPEED = 50
    TANK_ENEMY_Y = 80  # Posição Y fixa no topo da tela

    # PROJECTILE
    PROJECTILE_DEFAULT_SPEED = 800
    PROJECTILE_DEFAULT_FREQUENCY = 10
    PROJECTILE_DEFAULT_DAMAGE = 10
    PROJECTILE_DEFAULT_WIDTH = 8
    PROJECTILE_DEFAULT_HEIGHT = 8
    PROJECTILE_DEFAULT_COLOR = Colors.YELLOW

    # ABILITY
    ABILITY_WIDTH = 15
    ABILITY_HEIGHT = 15
    ABILITY_COOLDOWN = 10
    ABILITY_DEFAULT_COLOR = Colors.BLUE
    ABILITY_DURATION = 5
    ABILITY_DAMAGE = 50
    ABILITY_SPEED = 500
    MISSILE_SHOT_CAPACITY = 5
    ANGLE_SPREAD_MISSILE = 10
    EXPLOSION_RADIUS = 100
    COLOR_EXPLOSION = (255, 165, 0, 180)
    LASER_LIFETIME = 1 / 60
    LASER_DURATION = 8
    LASER_WIDTH = 5
    SEGMENT_LASER_LENGTH = 20
    COLOR_LASER = (255, 10, 60)
    COLOR_LASER_CORE = (255, 255, 255)
    GLOW_COLOR_LASER = (*COLOR_LASER, 150)
    NORMAL_SHOTS_REQUIRED = 5
    COLOR_GLOW_CRITICAL_SHOT = (255, 255, 180, 160)
    CRITICAL_SHOT_WIDTH_BORDER = 24
    CRITICAL_SHOT_HEIGHT_BORDER = 24
