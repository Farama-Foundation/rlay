import pytest
import gymnasium as gym
import numpy as np
from multiprocessing import Process
from rlay import ServerBackend, ClientEnv


class EmptyEnv(gym.Env):
    def __init__(self, obs_size: int = 4):
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(obs_size,), dtype=np.float32)
        self.action_space = gym.spaces.Discrete(2)
        self.zeros = np.zeros(obs_size, dtype=np.float32)

    def reset(self, seed: int | None = None, options: dict | None = None):
        return self.zeros, {}

    def step(self, action):
        return self.zeros, 0, False, False, {}


def run_server():
    gym.register("EmptyEnv-v0", entry_point=EmptyEnv)
    server = ServerBackend("EmptyEnv-v0", env_kwargs={"obs_size": 4})
    server.run()


def run_client():
    env = ClientEnv()
    env.reset()
    for _ in range(1_000):
        action = np.array([0], dtype=int)
        obs, reward, terminated, truncated, info = env.step(action)
        assert obs.shape == (4,)
        assert reward == 0
        assert not terminated
        assert not truncated
        assert info == {}
        if terminated or truncated:
            env.reset()
    env.close()


def test_environment_interaction():
    server_process = Process(target=run_server)
    server_process.start()

    client_process = Process(target=run_client)
    client_process.start()
    client_process.join()

    server_process.terminate()
    server_process.join()

