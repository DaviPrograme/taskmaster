from utils.CheckConfig.utils.classes.LevelSpec import LevelSpec
from utils.CheckConfig.utils.classes.DescriptionLevelError import DescriptionLevelError
from utils.sigs import sigs
import grp
import pwd
import os

#VERIFICACOES PARA CAMPOS ESPECIFICOS

def check_programs_field(CheckConfig, config_programs):
    if dict != type(config_programs):
        return CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), CheckConfig.throw_level_type_error()))
    for program_name in config_programs.keys():
        CheckConfig.levels.insert_next_level(LevelSpec(program_name, True))
        if type(config_programs[program_name]) != dict:
            CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), CheckConfig.throw_level_type_error()))
        else :
            CheckConfig.check_level_structure(config_programs[program_name])
        CheckConfig.check_required_fields_present_in_config(config_programs[program_name])
        CheckConfig.levels.delete_last_level()


def check_numprocs_field(CheckConfig, numprocs):
    if numprocs < 1:
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'numprocs' field must be a number greater than zero."))


# def check_umask_field(CheckConfig, umask):
#     try:
#         int(umask, 8)
#     except ValueError:
#         CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'umask' field must be in octal base."))

    
def check_autorestart_field(CheckConfig, autorestart):
    if type(autorestart) is str and autorestart != "unexpected":
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'autorestart' field can only be 'False', 'True' and 'unexpected'."))
    

def check_exitcodes_field(CheckConfig, exitcodes):
    for exitcode in exitcodes:
        if not type(exitcode) == int:
            CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'exitcodes' field has to be a list of ints."))

def check_startretries_field(CheckConfig, startretries):
    if startretries < 0:
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'startretries' field must be a positive number."))

def check_starttime_field(CheckConfig, starttime):
    if starttime < 0:
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'starttime' field must be a positive number."))


def check_stopsignal_field(CheckConfig, stopsignal):
    if not sigs.get(stopsignal, False):
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The value of the 'stopsignal' field is not a valid option."))


def check_stoptime_field(CheckConfig, stoptime):
    if stoptime < 0:
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'stoptime' field must be a positive number."))


def check_workingdir_field(CheckConfig, path):
    if not os.path.exists(path):
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The directory '{path}' was not found."))
    elif os.path.isfile(path):
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The path '{path}' must be a directory."))


def check_logfile_field(CheckConfig, path):
    if not os.path.exists(path):
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The file '{path}' was not found."))


def check_uid_field(CheckConfig, uid):
    try :
        pwd.getpwnam(uid).pw_uid
    except:
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'uid' not found."))


def check_gid_field(CheckConfig, gid):
    try :
        grp.getgrnam(gid).gr_gid
    except:
        CheckConfig.errors_tests_list.append(DescriptionLevelError(CheckConfig.levels.get_level_string(), f"The 'gid' not found."))


checks_field_functions = {
    "programs" : check_programs_field,
    "numprocs" : check_numprocs_field,
    # "umask": check_umask_field,
    "autorestart": check_autorestart_field,
    "exitcodes": check_exitcodes_field,
    "startretries": check_startretries_field,
    "starttime": check_starttime_field,
    "stopsignal": check_stopsignal_field,
    "stoptime": check_stoptime_field,
    "workingdir": check_workingdir_field,
    "logfile": check_logfile_field,
    "uid": check_uid_field,
    "gid": check_gid_field
}