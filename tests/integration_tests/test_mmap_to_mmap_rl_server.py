# from __future__ import annotations

# from multiprocessing import Process

# import numpy as np
# from tqdm import trange

# from rlay import ClientBackend, ServerEnv


# def run_server():
#     env = ServerEnv()
#     env.reset()
#     for _ in trange(1000):
#         action = np.array([0], dtype=int)
#         obs, reward, terminated, truncated, info = env.step(action)
#         if terminated or truncated:
#             env.reset()
#     env.close()


# def run_client():
#     server = ClientBackend("CartPole-v1")
#     server.run()


# def test_environment_interaction_T():
#     server_process = Process(target=run_server)
#     server_process.start()

#     client_process = Process(target=run_client)
#     client_process.start()
#     client_process.join()  # Wait for the client to finish

#     server_process.terminate()
#     server_process.join()

from __future__ import annotations

import os
import time

from tests.helper.processes import create_process_from_py_file

def test_environment_interaction():

    server_process = create_process_from_py_file(
        './examples/mmap_rl_server.py',
        {"PROFILINGFILE":"./tests/logs/profiling/mmap_to_mmap_rl_server.txt"}
    )
    client_process = create_process_from_py_file('./examples/mmap_env_client.py')
    
    assert(client_process.wait()==0)
    
    server_process.terminate()
    server_process.wait() 