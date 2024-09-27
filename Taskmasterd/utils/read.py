from utils.CheckConfig.CheckConfig import CheckConfig
from utils.insert_logs import insert_logs
import yaml
import os

def read_confs(path, confs):
    if not os.path.exists(path):
        err_str = f"The file {path} could not be readed because it does not exists"
        insert_logs("ERRO", err_str, confs)
        return {}, err_str
    with open(path) as conf_file:
            readed = yaml.safe_load(conf_file)
    check_config = CheckConfig()
    err_list = check_config.run(readed)
    if err_list:
        for err in err_list:
            insert_logs("ERRO", f"error were found in the configuration file: {err.error_text}.", confs)
        readed = {}
    return readed, err_list