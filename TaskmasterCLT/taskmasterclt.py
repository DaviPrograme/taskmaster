import curses
from utils.Commands import Commands
import requests
import signal
import sys
import os



def request_start(progs):
    
    url = "http://localhost:4242/start"

    payload = {"program": progs}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }   

    return requests.request("POST", url, json=payload, headers=headers)


def start_command(stdscr, progs):
    if not progs:
        print_line(stdscr, f"It is necessary to pass the name of the program")
        return

    try:
        response = request_start(progs)
    except:
        print_line(stdscr, f"error: taskmasterd is offline")
        return
    if response.status_code == 200:
        print_line(stdscr, f"success!")
    else:
        data = response.json()
        print_line(stdscr, f"error: group '{data['program']}' not found.")


def request_stop(progs):
    
    url = "http://localhost:4242/stop"

    payload = {"program": progs}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }   

    return requests.request("POST", url, json=payload, headers=headers)


def stop_command(stdscr, progs):
    if not progs:
        print_line(stdscr, f"It is necessary to pass the name of the program")
        return
    try:
        response = request_stop(progs)
    except:
        print_line(stdscr, f"error: taskmasterd is offline")
        return
    if response.status_code == 200:
        print_line(stdscr, f"success!")
    else:
        data = response.json()
        print_line(stdscr, f"error: group '{data['program']}' not found.")

def request_restart(progs):
    
    url = "http://localhost:4242/restart"

    payload = {"program": progs}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }   

    return requests.request("POST", url, json=payload, headers=headers)

def restart_command(stdscr, progs):
    if not progs:
        print_line(stdscr, f"It is necessary to pass the name of the program")
        return
    try:
        response = request_restart(progs)
    except:
        print_line(stdscr, f"error: taskmasterd is offline")
        return
    if response.status_code == 200:
        print_line(stdscr, f"success!")
    else:
        data = response.json()
        print_line(stdscr, f"error: group '{data['program']}' not found.")

def status_command(stdscr, progs):
    url = "http://localhost:4242/status"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }   
    try:
        response = requests.request("POST", url, headers=headers)
    except:
        print_line(stdscr, f"error: taskmasterd is offline")
        return
    y_old, _ = stdscr.getyx()
    clean_screen(stdscr, y_old)
    data = response.json()
    for prog in data.keys():
        for status, n in data[prog].items():
            s = "process" if n < 2 else "processes"
            print_line(stdscr, f"{prog}: {n} {s} {status}")

def shutdown_command(stdscr, progs):
    url = "http://localhost:4242/pid"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }   
    try:
        response = requests.request("GET", url, headers=headers)
    except:
        print_line(stdscr, f"error: taskmasterd is offline")
        return
    print_line(stdscr, f"Really shut the remote taskmasterd process down y/N?")
    key = stdscr.getch()
    if key == 121:
        json = response.json()
        pid = json.get('Response')
        os.kill(pid, signal.SIGINT)
        print_line(stdscr, f"Shut down")

def reload_command(stdscr, progs):
    url = "http://localhost:4242/pid"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }   
    try:
        response = requests.request("GET", url, headers=headers)
    except:
        print_line(stdscr, f"error: taskmasterd is offline")
        return
    
    json = response.json()
    pid = json.get('Response')
    os.kill(pid, signal.SIGHUP)
    print_line(stdscr, f"Reloaded taskmasterd")

def reread_command(stdscr, path):
    url = "http://localhost:4242/reread"

    payload = {"path": path}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }   
    try:
        response = requests.request("POST", url, json=payload, headers=headers)
    except:
        print_line(stdscr, f"error: taskmasterd is offline")
        return
    if response.status_code == 200:
        print_line(stdscr, f"readed")
    else:
        json = response.json()
        err_list = json.get('errors')
        for e in err_list:
            print_line(stdscr, f"ERROR: CANT_REREAD: {e}")

def update_command(stdscr, progs):
    url = "http://localhost:4242/update"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "taskmasterclt 1.0"
    }
    print_line(stdscr, f"Really restart the remote taskmasterd process y/N?")
    key = stdscr.getch()
    if key == 121:  
        try:
            response = requests.request("GET", url, headers=headers)
            print_line(stdscr, f"Restarted taskmasterd")
        except:
            print_line(stdscr, f"error: taskmasterd is offline")


def command_not_found(stdscr, command):
    if command: 
        print_line(stdscr, "command not found")


def print_line(stdscr, text):
    y_old, _ = stdscr.getyx()
    y_max, _ = stdscr.getmaxyx()
    if y_max <= y_old + 1:
        clean_screen(stdscr, y_old)
    stdscr.addstr(f"{text}\n")


valid_commands = {
    "start": start_command,
    "stop": stop_command,
    "restart": restart_command,
    "shutdown": shutdown_command,
    "reload": reload_command,
    "update": update_command,
    "reread": reread_command,
    "status": status_command
}

def move_cursor_left(y, x, start_x):
    new_x = start_x if x <= start_x else x - 1
    return  y, new_x


def move_cursor_right(y, x, x_max, len_command):
    new_x = len_command if x >= len_command else x + 1
    new_x = x_max - 1 if new_x >= x_max else new_x
    return  y, new_x


def clear_line(stdscr, y):
    stdscr.move(y, 0)
    stdscr.clrtoeol()


def clean_screen(stdscr, y):
    for y_now in range(y, -1, -1):
        clear_line(stdscr, y_now)


def is_printable(key):
    return key >= 32 and key <= 126


def right_action(stdscr, commands, key):
    y_old, x_old = stdscr.getyx()
    _, x_max = stdscr.getmaxyx()
    y, x = move_cursor_right(y_old, x_old, x_max, commands.len_line_now()) 
    stdscr.move(y, x)


def left_action(stdscr, commands, key):
    y_old, x_old = stdscr.getyx()
    y, x = move_cursor_left(y_old, x_old, commands.len_start_line_title()) 
    stdscr.move(y, x)


def up_action(stdscr, commands, key):
    y_old, _ = stdscr.getyx()
    commands.up_arrow_action()
    clear_line(stdscr, y_old)
    text = commands.build_line()
    stdscr.addstr(text)
    stdscr.move(y_old, len(text))


def down_action(stdscr, commands, key):
    y_old, _ = stdscr.getyx()
    commands.down_arrow_action()
    clear_line(stdscr, y_old)
    text = commands.build_line()
    stdscr.addstr(text)
    stdscr.move(y_old, len(text))


def del_action(stdscr, commands, key):
    y_old, x_old = stdscr.getyx()
    commands.delete_action(x_old)
    clear_line(stdscr, y_old)
    stdscr.addstr(commands.build_line())
    stdscr.move(y_old, x_old)


def backspace_action(stdscr, commands, key):
    y_old, x_old = stdscr.getyx()
    commands.backspace_action(x_old)
    clear_line(stdscr, y_old)
    stdscr.addstr(commands.build_line())
    x_new = x_old - 1 if commands.get_position_cursor_in_command_now(x_old) > 0  else x_old
    stdscr.move(y_old, x_new)


def enter_action(stdscr, commands, key):
    y_old, _ = stdscr.getyx()
    command = commands.trim_command_now()
    if command == "clear":
        clean_screen(stdscr, y_old)
        commands.enter_action()
        stdscr.addstr(commands.build_line())
    else:
        y_max, _ = stdscr.getmaxyx()
        if y_max <= y_old + 1:
            clean_screen(stdscr, y_old)
            y_old, _ = stdscr.getyx()
        clear_line(stdscr, y_old)
        print_line(stdscr, commands.build_line())
        split = command.split(sep=" ", maxsplit=1)
        func = valid_commands.get(split[0], None)
        if func:
            func(stdscr, "" if len(split) <= 1 else split[1])
        else:
            command_not_found(stdscr, command)
        commands.enter_action()
        stdscr.addstr(commands.build_line())


def write_action(stdscr, commands, key):
    y_old, x_old = stdscr.getyx()
    _, x_max = stdscr.getmaxyx()
    if is_printable(key) and x_old < x_max - 1:
        commands.insert_char_into_command_now(chr(key), x_old)
        clear_line(stdscr, y_old)
        stdscr.addstr(commands.build_line())
        x = x_old + 1
        stdscr.move(y_old, x)


KEY_ENTER = 10
actions = {
    curses.KEY_RIGHT:       right_action,
    curses.KEY_UP:          up_action,
    curses.KEY_DOWN:        down_action,
    curses.KEY_LEFT:        left_action,
    curses.KEY_DC:          del_action,
    curses.KEY_BACKSPACE:   backspace_action,
    KEY_ENTER:              enter_action
}
    

def main(stdscr):
    commands = Commands()
    stdscr.clear()
    stdscr.addstr(commands.build_line())

    while True:
        key = stdscr.getch()
        command = commands.trim_command_now()
        if key == KEY_ENTER and command == "exit":
            break
        action = actions.get(key, write_action)
        action(stdscr, commands, key)
        stdscr.refresh()

def sigint_handler(sig, frame):
        sys.exit()

signal.signal(signal.SIGINT, sigint_handler)
if __name__ == "__main__":
    curses.wrapper(main)