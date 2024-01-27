import numpy as np
from tqdm import trange

from rlay import ServerEnv
from tests.helper.profiler import Profiler

def run_mmap_rl_server(title:str=''):
    profiler = Profiler(["wall_time","step_time"])
    profiler.start_timer('wall_time')
    
    env = ServerEnv()
    env.reset()
    for i in trange(1_000):
        profiler.start_timer('step_time')
        action = np.array([0], dtype=int)
        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            env.reset()
        profiler.end_timer('step_time')

    env.close()

    profiler.end_timer('wall_time')
    profiler.save_profiling_stats_text(filename=title,message_timer_name='step_time',wall_timer_name='wall_time')   

if __name__ == "__main__":

    import os
    run_mmap_rl_server(os.environ['PROFILINGFILE'] or "mmap_rl_server")