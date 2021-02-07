# visual parameters
CAPTION = 'SCAREcrow: Sentinel Conservation via Aerial Reconnaissance and Escort'
ICON_PATH = 'assets/crow-skull-logo-removebg.png'
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800  # pixels
GRID_SIZE = 20  # pixels
KEEPOUT_SIZE = 20  # grids
DEFENDER_SIZE = 2
SUBJECT_SIZE = 10
SPOOK_COLOR = (255, 140, 0)
BREACH_COLOR = (255, 0, 0)
KEEPOUT_COLOR = (0, 0, 0)
SUBJECT_COLOR = (255, 0, 0)
DEFENDER_COLOR = (0, 0, 255)

# reinforcement learner parameters
ALGORITHM = 'Rules'  # 'DQN', 'PPO', 'Human', 'Rules'
TRAIN = False
NUM_EPISODES = 1000
MAX_STEPS = 100
DISCOUNT_FACTOR = 0.99
BATCH_SIZE = 32
SOFT_UPDATE = 100

# boids algorithm parameters
SUBJECT_FORCE = 0.5
SUBJECT_SPEED = 5
SUBJECT_PERCEPTION = 60
SPOOK_DISTANCE = 60
SPOOK_FORCE = 100

# game parameters
GAME_SPEED = 5  # fps
SUBJECT_COUNT = 4  # pigs
DEFENDER_COUNT = 1  # uavs
WIDTH_COUNT = int(SCREEN_WIDTH/GRID_SIZE)
HEIGHT_COUNT = int(SCREEN_HEIGHT/GRID_SIZE)
GRID_COUNT = WIDTH_COUNT * HEIGHT_COUNT
ACTION_MEANING = {0: 'still', 1: 'left', 2: 'right', 3: 'forward', 4: 'backward'}
