import io
import os
import subprocess

def create_process_from_py_file(pyfilepath:str, extra_env:dict={}, timeout:int=10, logging=False) -> subprocess.Popen:
    
    env = os.environ
    env['PYTHONPATH'] = os.getcwd() # this helps fix import errors

    if logging:
        os.makedirs(f'./tests/logs/{os.path.dirname(pyfilepath)}',exist_ok=True)
        with io.open(f'./tests/logs/{pyfilepath}.txt','w') as out:
            process = subprocess.Popen(
                ['timeout',str(timeout),'python',pyfilepath],
                stdout = out,
                stderr = subprocess.STDOUT,
                env = env | extra_env
            )
    else:
        process = subprocess.Popen(
            ['timeout',str(timeout),'python',pyfilepath],
            stderr = subprocess.STDOUT,
            env = env | extra_env
        )

    return process
