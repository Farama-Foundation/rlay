from __future__ import annotations

from multiprocessing import Process

import numpy as np
from tqdm import trange

from rlay import ClientBackend, ServerEnv


def run_server():
    env = ServerEnv()
    env.reset()
    for _ in trange(1000):
        action = np.array([0], dtype=int)
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            env.reset()
    env.close()


def run_client():
    server = ClientBackend("CartPole-v1")
    server.run()


def test_environment_interaction_T():
    server_process = Process(target=run_server)
    server_process.start()

    client_process = Process(target=run_client)
    client_process.start()
    client_process.join()  # Wait for the client to finish

    server_process.terminate()
    server_process.join()
