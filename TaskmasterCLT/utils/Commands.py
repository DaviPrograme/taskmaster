START_LINE_STR = "taskmasterCTL: "

class Commands:
    def __init__(self):
        self.command_now = ""
        self.__original = ""
        self.__index = 0
        self.__len = 0
        self.__max_len = 500
        self.__command_list = []

    def get_position_cursor_in_command_now(self, pos_x):
        return pos_x - len(START_LINE_STR)

    def insert_char_into_command_now(self, char, x):
        posicao = self.get_position_cursor_in_command_now(x)
        if posicao > 0 and posicao < len(self.command_now):
            self.command_now =  self.command_now[:posicao] + char + self.command_now[posicao:]
        elif posicao == 0:
            self.command_now = char + self.command_now
        elif posicao == len(self.command_now):
            self.command_now += char

    def backspace_action(self, x):
        posicao = self.get_position_cursor_in_command_now(x)
        if posicao > 0 and posicao < len(self.command_now):
            self.command_now = self.command_now[:posicao - 1] + self.command_now[posicao:]
        elif posicao == len(self.command_now) :
            self.command_now = self.command_now[:len(self.command_now) - 1]


    def delete_action(self, x):
        posicao = self.get_position_cursor_in_command_now(x)
        if posicao == 0:
            self.command_now = self.command_now[1:] 
        elif posicao > 0 and posicao < len(self.command_now):
            self.command_now = self.command_now[:posicao] + self.command_now[posicao + 1:]

    def get_next_command(self):
        if self.__command_list:
            self.command_now = self.__command_list[-self.__index]


    def up_arrow_action(self):
        if self.__index == 0:
            self.__original = self.command_now
        if self.__index < self.__len:
            self.__index += 1
        self.get_next_command()


    def down_arrow_action(self):
        if self.__index > 0:
            self.__index -= 1
            if self.__index > 0:
                self.get_next_command()
            else:
                self.command_now = self.__original


    def len_line_now(self):
        return len(START_LINE_STR + self.command_now)

    def len_start_line_title(self):
        return len(START_LINE_STR)

    def build_line(self):
        return START_LINE_STR + self.command_now

    def trim_command_now(self):
        return self.command_now.strip()

    def inc_len(self):
        if self.__len < self.__max_len:
            self.__len += 1

    def enter_action(self):
        if self.command_now:
            self.__command_list.append(self.command_now)
            self.inc_len()
            self.__index = 0
            self.command_now = ""
