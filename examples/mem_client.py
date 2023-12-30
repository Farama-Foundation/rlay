import numpy as np
from tqdm import trange

from rlay import ClientEnv


env = ClientEnv()

env.reset()
for i in trange(100_000):
    # print(i)
    action = np.array([0], dtype=int)
    obs, reward, terminated, truncated, info = env.step(action)
    # print(obs)
    if terminated or truncated:
        env.reset()

env.close()
