class Colors:
    WHITE = (255, 255, 255)
    GLOW_WHITE = (255, 255, 255, 200)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    RED_GLOW = (255, 0, 0, 10)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (125, 249, 255)
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

class Sounds:
    # MUSIC
    PLAY = "play"

    # SOUND EFFECTS
    BOOM = "boom"
    CLICK = "click"
    CRITICAL_SHOT = "critical shot"
    DEATH = "death"
    GAME_OVER = "game over"
    GUN_SHOT = "gun shot"
    HIT = "hit"
    LAUNCHER = "launcher"
    LASER_BEAM = "laser beam"
    LASER_SHOT = "laser shot"
    PLASMA = "plasma"
    RECHARGED = "recharged"
    STOMP = "stomp"

class Constants:
    # GENERAL
    FPS = 60
    WIDTH = 1280
    HEIGHT = 720
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
    PLAYER_WIDTH = 100
    PLAYER_HEIGHT = 100
    PLAYER_SPEED = 200
    PLAYER_DEFAULT_COLOR = Colors.DARK_GRAY
    JUMP_SPEED = 700
    PLAYER_MAX_HEALTH = 100

    # ENEMIES
    MAX_ENEMIES = 20
    ENEMY_SPEED = 100
    # SPAWN
    SPAWN_TIMER = 2.5
    WAVY_ENEMY_SPAWN_CHANCE = 100 * 0.3
    LINEAR_ENEMY_SPAWN_CHANCE = 100 * 0.3
    BOUNCING_ENEMY_SPAWN_CHANCE = 100 * 0.25
    TANK_ENEMY_SPAWN_CHANCE = 100 * 0.15
    # WAVY ENEMY
    WAVY_ENEMY_WIDTH = 128
    WAVY_ENEMY_HEIGHT = 121.8
    WAVY_ENEMY_PROJECTILE_WIDTH = 15
    WAVY_ENEMY_PROJECTILE_HEIGHT = 15
    WAVY_ENEMY_Y = 100
    WAVY_ENEMY_AMPLITUDE = 100
    WAVY_ENEMY_ANGULAR_FREQUENCY = 3
    WAVY_ENEMY_MAX_HEALTH = 100
    WAVY_ENEMY_SPEED = 1.0 * ENEMY_SPEED
    # LINEAR ENEMY
    LINEAR_ENEMY_WIDTH = 119.1
    LINEAR_ENEMY_HEIGHT = 94.35
    LINEAR_ENEMY_PROJECTILE_WIDTH = 15
    LINEAR_ENEMY_PROJECTILE_HEIGHT = 15
    LINEAR_ENEMY_MAX_HEALTH = 80
    LINEAR_ENEMY_SPEED = 150
    # BOUNCING ENEMY
    BOUNCING_ENEMY_WIDTH = 131.25
    BOUNCING_ENEMY_HEIGHT = 75.6
    BOUNCING_ENEMY_MAX_HEALTH = 60
    BOUNCING_ENEMY_HORIZONTAL_SPEED = 150
    BOUNCING_ENEMY_FALL_SPEED = 1000
    BOUNCING_ENEMY_RISE_SPEED = 100
    BOUNCING_ENEMY_BASE_HEIGHT = HEIGHT / 4
    BOUNCING_ENEMY_MIN_TIME_BEFORE_FALL = 2
    BOUNCING_ENEMY_MAX_TIME_BEFORE_FALL = 5
    BOUNCING_ENEMY_WAIT_TIME = 1
    BOUNCING_ENEMY_FALL_DAMAGE = 2
    # TANK ENEMY
    TANK_ENEMY_WIDTH = 188.8
    TANK_ENEMY_HEIGHT = 121.4
    TANK_ENEMY_MAX_HEALTH = 1000
    TANK_ENEMY_SPEED = 50
    TANK_ENEMY_Y = 80
    TANK_ENEMY_SHOOT_FREQUENCY = 2
    TANK_BOMB_WIDTH = 30
    TANK_BOMB_HEIGHT = 30
    TANK_BOMB_SPEED = 200
    TANK_BOMB_DAMAGE = 30
    TANK_BOMB_EXPLOSION_RADIUS = 100
    TANK_BOMB_EXPLOSION_COLOR = (71,151,160,255)

    # PROJECTILE
    PROJECTILE_DEFAULT_SPEED = 800
    PROJECTILE_DEFAULT_FREQUENCY = 10
    PROJECTILE_DEFAULT_DAMAGE = 10
    PROJECTILE_DEFAULT_WIDTH = 8
    PROJECTILE_DEFAULT_HEIGHT = 8
    PROJECTILE_DEFAULT_COLOR = Colors.YELLOW

    # ABILITIES
    ABILITY_DEFAULT_COLOR = Colors.BLUE
    ABILITY_DEFAULT_DAMAGE = 50
    ABILITY_DEFAULT_SPEED = 500
    # MISSILE BARRAGE
    MISSILE_DAMAGE = 50
    MISSILE_SPEED = 1.5 * ABILITY_DEFAULT_SPEED
    MISSILE_SHOT_CAPACITY = 5
    ANGLE_SPREAD_MISSILE = 10
    MISSILE_COOLDOWN = 5
    MISSILE_LIFETIME = 10 * WIDTH / ABILITY_DEFAULT_SPEED
    EXPLOSION_RADIUS = 100
    COLOR_EXPLOSION = (255, 165, 0, 180)
    # LASER BEAM
    LASER_DAMAGE = 2 * ABILITY_DEFAULT_DAMAGE
    LASER_SPEED = ABILITY_DEFAULT_SPEED
    LASER_DURATION = 5
    LASER_COOLDOWN = 8
    LASER_LIFETIME = 1 / 60
    HIT_LIFETIME = 0.5
    LASER_WIDTH = 5
    LASER_TIME_DIVISOR = 500
    LIMIT_WIDTH_LASER = WIDTH * 9
    SEGMENT_LASER_LENGTH = 20 * 0.8
    COLOR_LASER = (255, 10, 60)
    COLOR_LASER_CORE = (255, 255, 255)
    GLOW_COLOR_LASER = (*COLOR_LASER, 150)
    # CRITICAL SHOT
    CRITICAL_DAMAGE = 3 * ABILITY_DEFAULT_DAMAGE
    CRITICAL_SHOT_SPEED = 3 * ABILITY_DEFAULT_SPEED
    CRITICAL_SHOT_COOLDOWN = 8
    NORMAL_SHOTS_REQUIRED = 10
    COLOR_GLOW_CRITICAL_SHOT = (255, 255, 180, 100)
    CRITICAL_SHOT_WIDTH_BORDER = 24
    CRITICAL_SHOT_HEIGHT_BORDER = 24
    CRITICAL_SHOT_LIFETIME = WIDTH / ABILITY_DEFAULT_SPEED
