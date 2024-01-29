from __future__ import annotations

import gymnasium as gym
import numpy as np

class EmptyEnv(gym.Env):
    def __init__(self, obs_size: int = 4):
        self.observation_space = gym.spaces.Box(
            low=0, high=1, shape=(obs_size,), dtype=np.float32
        )
        self.action_space = gym.spaces.Discrete(2)
        self.zeros = np.zeros(obs_size, dtype=np.float32)

    def reset(self, seed: int | None = None, options: dict | None = None):
        return self.zeros, {}

    def step(self, action):
        return self.zeros, 0, False, False, {}