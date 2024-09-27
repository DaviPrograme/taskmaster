from utils.start import start_program
from utils.stop import stop_program
from utils.insert_logs import insert_logs
import copy

def update_confs(confs, procs, readed):

    to_updade = []

    for prog in confs['programs'].keys():
        for key, value in confs['programs'][prog].items():
            if readed['programs'].get(prog, {}).get(key) != value:
                to_updade.append(prog)
                break
    
    for prog in readed['programs'].keys():
        if not confs['programs'].get(prog, {}):
            to_updade.append(prog)

    for prog in to_updade:
        if confs['programs'].get(prog, {}):
            for p in procs[prog].values():
                p['default'] = False
            stop_program(prog, confs, procs)
            del procs[prog]
        if readed['programs'].get(prog, {}):
            procs[prog] = {}
            start_program(prog, readed, procs)
        insert_logs("WARN",f"the program '{prog}' has been reloaded", confs)

    confs.clear()
    confs.update(copy.deepcopy(readed))
    