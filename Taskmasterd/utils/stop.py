from utils.sigs import sigs
import signal
import os
import subprocess
from utils.insert_logs import insert_logs

def is_process_active(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def stop_program(prog, confs, procs):
        stop_time = confs['programs'][prog].get('stoptime', 10)
        signal = sigs[confs['programs'][prog].get('stopsignal', 'TERM')]
        to_stop = {pid: procs[prog][pid] for pid in procs.get(prog, {}).keys()}
        if to_stop:
            for pid in to_stop.keys():
                if to_stop[pid]['status'] == None:
                    insert_logs("INFO", f"starting to stop the process {prog}_{pid}", confs)
                    ret = os.kill(pid, signal)
                    try:
                        to_stop[pid]['process'].wait(timeout=stop_time)
                    except subprocess.TimeoutExpired:
                        os.kill(pid, sigs['KILL'])
                    if not is_process_active(pid):
                        insert_logs("INFO", f"success: process {prog}_{pid} stopped", confs)
                        to_stop[pid]['status'] = 'STOPPED'
                    else:
                        insert_logs("CRIT", f"error: unable to stop the process {prog}_{pid}", confs)