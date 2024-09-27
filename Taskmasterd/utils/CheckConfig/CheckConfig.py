from utils.CheckConfig.utils.standard_structure import standard_structure
from utils.CheckConfig.utils.classes.LevelList import LevelList
from utils.CheckConfig.utils.classes.LevelSpec import LevelSpec
from utils.CheckConfig.utils.classes.DescriptionLevelError import DescriptionLevelError
from utils.CheckConfig.utils.funcs.throw_errors_funcs import errors_funcs

class CheckConfig():
    def __init__(self):
        self.levels = LevelList()
        self.errors_tests_list = []


    def print_levels(self):
        for level in self.errors_tests_list:
            print(f"field: {level.field}\nmsg: {level.error_text}\n\n")


    def get_field_in_standard_level_structure(self):
        structure = standard_structure
        now_level = None
        for level_name in [level.level_name for level in self.levels.list if level.is_custom_name == False] :
            now_level = structure.get(level_name, None)
            if now_level and now_level["level_type"] == dict and not now_level.get("is_env", False):
                structure = now_level["fields"]
        return now_level


    def check_required_fields_present_in_config(self, level_now_config):
        standard_structure_here = self.get_field_in_standard_level_structure()
        set_A = {field_name for field_name in standard_structure_here["fields"].keys()}
        set_B = {field_name for field_name in level_now_config.keys()}
        intersec = set_A.intersection(set_B)
        for field_name in set_A.difference(intersec):
            if standard_structure_here["fields"][field_name]["is_required"]:
                self.errors_tests_list.append(DescriptionLevelError(self.levels.get_level_string(), errors_funcs["mandatory_field_not_found"](self, field_name)))

    
    def check_type_field(self, level_standard, content_level):
        if type(level_standard["level_type"]) is list:
            for next_type in level_standard["level_type"]:
                if next_type is type(content_level):
                    return True
            return False
        return level_standard["level_type"] is type(content_level)


    def check_level_structure(self, level_now_content):
        for field_name in level_now_content.keys():
            self.levels.insert_next_level(LevelSpec(field_name, False))
            level_exists = self.get_field_in_standard_level_structure()
            if not level_exists:
                self.errors_tests_list.append(DescriptionLevelError(self.levels.get_level_string(), errors_funcs["unrecognized_field"](self)))
            elif not self.check_type_field(level_exists, level_now_content[field_name]):
                self.errors_tests_list.append(DescriptionLevelError(self.levels.get_level_string(), errors_funcs["level_type"](self)))
            else :
                if  level_exists.get("check_func", False):
                    level_exists["check_func"](self, level_now_content[field_name])
                elif type(level_now_content[field_name]) == dict and not level_exists.get("is_env", False):
                    self.check_level_structure(level_now_content[field_name])
                    self.check_required_fields_present_in_config(level_now_content[field_name])
            self.levels.delete_last_level()


    def run(self, config):
        self.check_level_structure(config)
        self.print_levels()
        return self.errors_tests_list
