import signal

sigs = {
    'TERM': signal.SIGTERM,
    'KILL': signal.SIGKILL,
    'HUP': signal.SIGHUP,
    'INT': signal.SIGINT,
    'QUIT': signal.SIGQUIT,
    'ABRT': signal.SIGABRT,
    'ALRM': signal.SIGALRM,
    'USR1': signal.SIGUSR1,
    'USR2': signal.SIGUSR2,
    'STOP': signal.SIGSTOP,
    'CONT': signal.SIGCONT,
    'TSTP': signal.SIGTSTP,
    'TTIN': signal.SIGTTIN,
    'TTOU': signal.SIGTTOU,
    'PIPE': signal.SIGPIPE,
    'CHLD': signal.SIGCHLD,
    'WINCH': signal.SIGWINCH,
    'URG': signal.SIGURG,
    'POLL': signal.SIGPOLL,
    'PWR': signal.SIGPWR,
    'SYS': signal.SIGSYS
}