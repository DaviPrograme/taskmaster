import os
import sys

def daemonize():
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    os.setsid()
    os.umask(0)

    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    sys.stdout.flush()
    sys.stderr.flush()
    with open('/dev/null', 'r') as dev_null:
        os.dup2(dev_null.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'a+') as dev_null:
        os.dup2(dev_null.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'a+') as dev_null:
        os.dup2(dev_null.fileno(), sys.stderr.fileno())