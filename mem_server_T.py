from rlay import ServerEnv

import numpy as np
from tqdm import trange
env = ServerEnv()

env.reset()
for i in trange(100_000):
    # print(i)
    action = np.array([0], dtype=int)
    # breakpoint()
    obs, reward, terminated, truncated, info = env.step(action)
    # print(obs)
    if terminated or truncated:
        env.reset()

env.close()
