from __future__ import annotations

import gymnasium as gym
import numpy as np

from rlay import ServerBackend


class EmptyEnv(gym.Env):
    def __init__(self, obs_size: int = 4):
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(obs_size,), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(2)
        self.zeros = np.zeros(obs_size, dtype=np.float32)
        print(f"Obs size: {obs_size}")

    def reset(self, seed: int | None = None, options: dict | None = None):
        return self.zeros, {}

    def step(self, action):
        return self.zeros, 0, False, False, {}


gym.register("EmptyEnv-v0", entry_point=EmptyEnv)

server = ServerBackend("EmptyEnv-v0", env_kwargs={"obs_size": 4})
server.run()
