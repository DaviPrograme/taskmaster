from utils.CheckConfig.utils.funcs.check_level_funcs import checks_field_functions

standard_structure = {
    "taskmaster":{
        "fields": {
            "logfile" : {
                "level_type": str, 
                "is_required" : False,
                "check_func": checks_field_functions["logfile"]
            },
            "email" : {
                "level_type": str, 
                "is_required" : False
            },
            "uid" : {
                "level_type": str, 
                "is_required" : False,
                "check_func": checks_field_functions["uid"]
            },
            "gid" : {
                "level_type": str, 
                "is_required" : False,
                "check_func": checks_field_functions["gid"]
            },
        },
        "level_type": dict, 
        "is_required" : False,
    },
    "programs" : {
        "fields" : {
            "cmd" : {
                "level_type": str, 
                "is_required" : True
            },
            "numprocs" : {
                "level_type": int, 
                "is_required" : False,
                "check_func": checks_field_functions["numprocs"]
            },
            "umask" : {
                "level_type": int, 
                "is_required" : False,
            },
            "workingdir" : {
                "level_type": str, 
                "is_required" : False,
                "check_func": checks_field_functions["workingdir"]
            },
            "autostart" : {
                "level_type": bool, 
                "is_required" : False
            },
            "autorestart" : {
                "level_type": [str, bool], 
                "is_required" : False,
                "check_func": checks_field_functions["autorestart"]
            },
            "exitcodes" : {
                "level_type": list, 
                "is_required" : False,
                "check_func": checks_field_functions["exitcodes"]
            },
            "startretries" : {
                "level_type": int, 
                "is_required" : False,
                "check_func": checks_field_functions["startretries"]
            },
            "stopsignal" : {
                "level_type": str, 
                "is_required" : False
            },
             "stdout" : {
                "level_type": str, 
                "is_required" : False,
            },
            "stderr" : {
                "level_type": str, 
                "is_required" : False,
            },
            "starttime" : {
                "level_type": int, 
                "is_required" : False,
                "check_func": checks_field_functions["starttime"]
            },
            "stopsignal" : {
                "level_type": str, 
                "is_required" : False,
                "check_func": checks_field_functions["stopsignal"]
            },
            "stoptime" : {
                "level_type": int, 
                "is_required" : False,
                "check_func": checks_field_functions["stoptime"]
            },
            "env" : {
                "level_type": dict,
                "is_required" : False,
                "is_env": True
            },
        },
        "level_type": dict, 
        "is_required" : True,
        "check_func": checks_field_functions["programs"]
    }
} 