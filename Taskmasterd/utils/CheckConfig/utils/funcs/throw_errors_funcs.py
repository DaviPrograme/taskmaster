
def throw_unrecognized_field_error(CheckConfig):
    return f"The field located in the path '{CheckConfig.levels.get_level_string()}' was not recognized by the program."

def throw_level_type_error(CheckConfig):
    return f"The field located in the path '{CheckConfig.levels.get_level_string()}' has the wrong type."

def throw_mandatory_field_not_found_error(CheckConfig, field_name):
    return f"The field '{field_name}' which is mandatory was not found in the path '{CheckConfig.levels.get_level_string()}'."


errors_funcs = {
    "unrecognized_field": throw_unrecognized_field_error,
    "level_type": throw_level_type_error,
    "mandatory_field_not_found": throw_mandatory_field_not_found_error
}