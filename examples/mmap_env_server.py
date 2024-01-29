import gymnasium as gym

from rlay import ServerBackend
from tests.helper.environments import EmptyEnv

def run_mmap_env_server():
    gym.register("EmptyEnv-v0", entry_point=EmptyEnv)
    server = ServerBackend("EmptyEnv-v0", env_kwargs={"obs_size": 4})
    server.run()

if __name__ == "__main__":

    run_mmap_env_server()