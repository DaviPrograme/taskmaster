
def get_status(status):
    if status is None:
        return "RUNNING"
    if isinstance(status, int):
        return "EXITED"
    return status