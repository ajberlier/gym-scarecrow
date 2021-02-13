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
ALGORITHM = 'Human'  # 'Qlearn', 'Human', 'Rules'| Coming Soon: 'DQN', 'PPO'
HARDWARE = True
TRAIN = True
MAX_STEPS = 10  # steps of the simulation in an episode
NUM_EPISODES = 2  # total number of episodes run
# Qlearn params
ALPHA = 0.1  # learning rate
GAMMA = 0.6  # discount factor
EPSILON = 0.99  # percent of actions taken at random
EPSILON_DECAY = 0.99  # rate of decay for epsilon to trade off random exploration for exploitation on value function
PLAY_QTABLE = ''
OBS_GRID_SIZE_W = 240
OBS_GRID_SIZE_H = 160
OBS_WIDTH_COUNT = int(SCREEN_WIDTH/OBS_GRID_SIZE_W)
OBS_HEIGHT_COUNT = int(SCREEN_HEIGHT/OBS_GRID_SIZE_H)
OBS_GRID_COUNT = OBS_WIDTH_COUNT * OBS_HEIGHT_COUNT

# boids algorithm parameters
SUBJECT_FORCE = 0.5
SUBJECT_SPEED = 5
SUBJECT_PERCEPTION = 60
SPOOK_DISTANCE = 60
SPOOK_FORCE = 100

# game parameters
START_POSITION = [int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2)]
GAME_SPEED = 5  # fps
SUBJECT_COUNT = 5  # pigs
DEFENDER_COUNT = 1  # uavs
WIDTH_COUNT = int(SCREEN_WIDTH/GRID_SIZE)
HEIGHT_COUNT = int(SCREEN_HEIGHT/GRID_SIZE)
GRID_COUNT = WIDTH_COUNT * HEIGHT_COUNT
ACTION_MEANING = {0: 'still', 1: 'left', 2: 'right', 3: 'forward', 4: 'backward'}

# hardware parametetrs
STEP_DISTANCE = 1  # meter
