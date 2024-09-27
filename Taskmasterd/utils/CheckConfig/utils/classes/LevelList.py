
class LevelList():
    def __init__(self):
        self.list = []

    def insert_next_level(self, level_spec):
        self.list.append(level_spec)

    def delete_last_level(self):
        self.list.pop()

    def clear_level(self):
        self.list.clear()

    def get_level_string(self):
        string = ""
        count_levels = len(self.list)
        for index, level in enumerate(self.list):
            string = string + level.level_name
            if index + 1 < count_levels:
                string = string + "->"
        return string

    def print_levels(self):
        for level in self.list:
            print(f"field: {level.field}\nmsg: {level.error_text}\n\n")