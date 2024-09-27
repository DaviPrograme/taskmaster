import subprocess
import os
import threading
import time
import fcntl
from utils.insert_logs import insert_logs

def remove_stopped_process(prog, procs):
    to_delete = []
    for pid in procs.get(prog, {}).keys():
        if procs[prog][pid]['status'] is not None:
            to_delete.append(pid)
    for pid in to_delete:
        del procs[prog][pid]

def start_process(prog, confs, env):
    command = confs['programs'][prog]['cmd'].split()
    n_env = {key: str(value) for key, value in confs['programs'][prog].get('env', {}).items()}
    env.update(n_env)
    
    with open(confs['programs'][prog]['stdout'], 'a') as stdout_file, open(confs['programs'][prog]['stderr'], 'a') as stderr_file:
        cwd = confs['programs'][prog].get('workingdir', os.getcwd())
        umask = confs['programs'][prog].get('umask', 0o022)
        
        fcntl.flock(stdout_file, fcntl.LOCK_EX)
        fcntl.flock(stderr_file, fcntl.LOCK_EX)
        ret = subprocess.Popen(
            command,
            start_new_session=True,
            env=env,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
            cwd=cwd,
            umask=umask
        )
        fcntl.flock(stdout_file, fcntl.LOCK_UN)
        fcntl.flock(stderr_file, fcntl.LOCK_UN)
    return ret

def monitor_process(process, prog, confs, procs):
    auto_restart = confs['programs'][prog].get('autorestart', 'unexpected')
    exit_codes = confs['programs'][prog].get('exitcodes', [0])
    if not isinstance(exit_codes, list):
        exit_codes = [exit_codes]
    while True:
        status = process.poll()
        if status is not None:
            if procs[prog][process.pid].get('default', True):
                procs[prog][process.pid]['status'] = status
                if auto_restart == 'unexpected':
                    return_code = process.returncode
                    if return_code not in exit_codes:
                        insert_logs("CRIT", f"process {prog}_{process.pid} terminated unexpectedly", confs)
                        del procs[prog][process.pid]
                        insert_logs("INFO", f"restarting the {prog} group process", confs)
                        start_program(prog, confs, procs, is_restart=True)
                elif auto_restart is True:
                    del procs[prog][process.pid]
                    insert_logs("INFO", f"restarting the {prog} group process", confs)
                    start_program(prog, confs, procs, is_restart=True)
                elif auto_restart is False and process.returncode not in exit_codes:
                    insert_logs("CRIT", f"process {prog}_{process.pid} terminated unexpectedly", confs)
            break
    time.sleep(1)


def create_proc(prog, confs, procs, start_retries, start_time, env, lock):
    for j in range(start_retries + 1):
        try:
            ret_proc = start_process(prog, confs, env)
            insert_logs("INFO", f"spawned: {prog}_{ret_proc.pid} with pid {ret_proc.pid}", confs)
        except Exception as e:
            continue
        try:
            with lock:
                procs[prog].update({ret_proc.pid: {'process': ret_proc, 'status': 'STARTING'}})
            ret_proc.wait(timeout=start_time)
            insert_logs("ERRO", f"exited: {prog}_{ret_proc.pid} (exit status {ret_proc.poll()}; not expected)", confs)
            ret_proc.terminate()
            with lock:
                del procs[prog][ret_proc.pid]
            continue
        except subprocess.TimeoutExpired:
            insert_logs("INFO", f"success: {prog}_{ret_proc.pid} entered RUNNING state, process has stayed up for > than {start_time} seconds (starttime)", confs)
            with lock:
                procs[prog][ret_proc.pid]['status'] = ret_proc.poll()
                procs[prog][ret_proc.pid]['name'] = f"{prog}_{ret_proc.pid}"
        monitor_thread = threading.Thread(target=monitor_process, args=(ret_proc, prog, confs, procs), daemon=True)
        monitor_thread.start()
        return
    insert_logs("CRIT", f"exited: Unable to upload the {prog} process after {start_retries} attempts", confs)


def start_program(prog, confs, procs, is_restart=False):

    if not is_restart:
        remove_stopped_process(prog, procs)

    env = os.environ.copy()
    numprocs = confs['programs'][prog].get('numprocs', 1)
    start_retries = confs['programs'][prog].get('startretries', 0)
    start_time = confs['programs'][prog].get('starttime', 10)
    procs_to_start = numprocs - len(procs[prog])
    if is_restart is True:
        procs_to_start = 1
    lock = threading.Lock()
    for i in range(procs_to_start):
        monitor_thread = threading.Thread(target=create_proc, args=(prog, confs, procs, start_retries, start_time, env, lock), daemon=True)
        monitor_thread.start()
