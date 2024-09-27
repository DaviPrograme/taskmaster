from datetime import datetime
from utils.send_alert import send_alert
import fcntl


def insert_logs(status, text, confs):
    log_file = confs.get('taskmaster', {}).get('logfile', './logs/taskmasterd.log')
    with open(log_file, 'a') as stdout_file:
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fcntl.flock(stdout_file, fcntl.LOCK_EX)
        stdout_file.write(f"{data} {status} {text}\n")
        fcntl.flock(stdout_file, fcntl.LOCK_UN)
        if status is "CRIT" and confs.get('taskmaster', {}).get('email', None):
            send_alert(log_file, confs['taskmaster']['email'], f"{status} {text}")