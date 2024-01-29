import numpy as np

from rlay import ClientEnv
from tests.helper.profiler import Profiler

def run_mmap_rl_client(title:str=''):
    profiler = Profiler(["wall_time","step_time"])
    profiler.start_timer('wall_time')

    env = ClientEnv()
    env.reset()
    for _ in range(1_000):
        profiler.start_timer('step_time')
        action = np.array([0], dtype=int)
        obs, reward, terminated, truncated, info = env.step(action)
        assert obs.shape == (4,)
        assert reward == 0
        assert not terminated
        assert not truncated
        assert info == {}
        if terminated or truncated:
            env.reset()
        profiler.end_timer('step_time')
    env.close()
    
    profiler.end_timer('wall_time')
    profiler.save_profiling_stats_text(filename=title,message_timer_name='step_time',wall_timer_name='wall_time')   

if __name__=="__main__":

    import os
    run_mmap_rl_client(os.environ['PROFILINGFILE'] or "mmap_rl_client")