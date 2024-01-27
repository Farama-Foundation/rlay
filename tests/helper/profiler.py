import numpy as np
import os
import time
from typing import List
import scipy.stats as ss

class Profiler:
    """Convenience class for calculating wall time averages."""

    def __init__(self, timer_names:List[float]):

        self.durations = { timer_name:[] for timer_name in timer_names }
        self.timers = { timer_name:None for timer_name in timer_names }

    def start_timer(self, timer_name:str):
        """Start a timer for the given timer name."""

        if timer_name not in self.timers:
            raise Exception(f'Unknown timer name: "{timer_name}"')
        self.timers[timer_name] = time.time()

    def end_timer(self, timer_name:str) -> float:
        """Halt a timer and save the duration since starting the timer."""

        if timer_name not in self.timers:
            raise Exception(f'Unknown timer name: "{timer_name}"')
        if self.timers[timer_name] is None:
            raise Exception("A timer must be started before it can be ended!")

        self.durations[timer_name].append( time.time() - self.timers[timer_name] )
        self.timers[timer_name] = None
        return self.durations[timer_name][-1]
    
    def get_profiling_stats_text(self, message_timer_name:str, wall_timer_name:str) -> str:
        '''Print average messaging rates, durations, etc. for an array of messaging times.

        The rough average on chess moves per game is based on this thread:
        https://chess.stackexchange.com/questions/2506/what-is-the-average-length-of-a-game-of-chess

        All confidence intervals are calculated based at the 95% level.
        TODO: Confirm messages are Normally distributed
        '''

        n = len(self.durations[message_timer_name])
        times = np.array(self.durations[message_timer_name])
        
        dur = np.mean(times)
        dur_conf = np.std(times, ddof=1) * ss.t.ppf(.975,n-1) / np.sqrt(n)
        
        rate = np.mean(1 / times)
        rate_conf = np.std(1 / times, ddof=1) * ss.t.ppf(.975,n-1) / np.sqrt(n)

        return (
            f"Wall time: {1_000*self.durations[wall_timer_name][0]:.4f} ms\n"
            f"Message count: {n:,.0f} messages\n"
            f"Message rate: {rate:,.0f} ± {rate_conf:,.0f} messages/second\n"
            f"Message duration: {1_000_000*dur:.2f} ± {1_000_000*dur_conf:.2f} μs\n"
            f"Mean chess games per second: {rate/40:,.0f} ± {rate_conf/40:,.0f} games (40 moves/game on average)"
        )

    def save_profiling_stats_text(self, filename:str, message_timer_name:str, wall_timer_name:str):

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename,'w') as f:
            f.write(self.get_profiling_stats_text(message_timer_name,wall_timer_name))