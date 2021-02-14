from gym.envs.registration import register

register(
    id='Scarecrow-v0',
    entry_point='gym_scarecrow.envs:ScarecrowEnv',
    )
