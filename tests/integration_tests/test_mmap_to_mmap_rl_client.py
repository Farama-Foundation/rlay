from __future__ import annotations

import os
import time

from tests.helper.processes import create_process_from_py_file

def test_environment_interaction():

    server_process = create_process_from_py_file('./examples/mmap_env_server.py')
    client_process = create_process_from_py_file(
        './examples/mmap_rl_client.py',
        {"PROFILINGFILE":"./tests/logs/profiling/mmap_to_mmap_rl_client.txt"}
    )
    
    assert(client_process.wait()==0)
    
    server_process.terminate()
    server_process.wait() 