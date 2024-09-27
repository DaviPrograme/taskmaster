import pwd
import grp
import os
import sys
from utils.insert_logs import insert_logs

def privilege_descalation(confs):
    
    if os.geteuid() != 0:
        return

    uid_name = confs.get("taskmaster", {}).get("uid", None)
    gid_name = confs.get("taskmaster", {}).get("gid", None)

    if not uid_name or not gid_name:
        insert_logs("CRIT", "Taskmaster can't run as root. If you intend to run as root, you can set uid=root and gid=root in the config file to avoid this message.", confs)
        print("Taskmasterd can't run as root. If you intend to run as root, you can set uid=root and gid=root in the config file to avoid this message.")
        sys.exit(1)

    
    uid = pwd.getpwnam(uid_name).pw_uid
    gid = grp.getgrnam(gid_name).gr_gid

    os.setgid(gid)
    os.setgroups([])

    os.setuid(uid)

    os.umask(0o077)
   