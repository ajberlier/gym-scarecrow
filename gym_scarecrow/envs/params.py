# visual parameters
CAPTION = 'SCAREcrow: Sentinel Conservation via Aerial Reconnaissance and Escort'
ICON_PATH = 'assets/crow-skull-logo-removebg.png'
SCREEN_HEIGHT, SCREEN_WIDTH = 800, 1200  # pixels
GRID_SIZE = 20  # pixels
KEEPOUT_SIZE = 20  # grids
DEFENDER_SIZE = 10
SUBJECT_SIZE = 10
SPOOK_COLOR = (255, 140, 0)
BREACH_COLOR = (255, 0, 0)
KEEPOUT_COLOR = (0, 0, 0)
SUBJECT_COLOR = (255, 0, 0)
DEFENDER_COLOR = (0, 0, 255)

# reinforcement learner parameters
DISCOUNT_FACTOR = 0.99
MIN_EXPLORE_RATE = 0.001
MIN_LEARNING_RATE = 0.2
DECAY_FACTOR = 10
NUM_EPISODES = 9999999
MAX_T = 2000

# boids algorithm parameters
SUBJECT_FORCE = 0.5
SUBJECT_SPEED = 5
SUBJECT_PERCEPTION = 60
SPOOK_DISTANCE = 60
SPOOK_FORCE = 100

# game parameters
GAME_SPEED = 5  # fps
SUBJECT_COUNT = 10  # pigs
DEFENDER_COUNT = 2  # uavs
GRID_COUNT = int(SCREEN_HEIGHT/GRID_SIZE * SCREEN_WIDTH/GRID_SIZE)
