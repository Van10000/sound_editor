import functools

from ConsoleSoundEditor.ConsoleModel import ConsoleModel as CM


class CommandExecutor:
    def __init__(self, console_model):
        self.model = console_model
        self.command_funcs = dict()
        self.command_helps = dict()
        self.is_finished = False
        self.add_all_commands()

    def add_command(self, name, func, help_message):
        self.command_funcs[name] = func
        self.command_helps[name] = help_message

    def execute(self, raw_command):
        command = CommandExecutor.parse_command(raw_command)
        if len(command) == 0:
            return
        command_type = command[0]
        try:
            command_func = self.command_funcs[command_type]
        except KeyError:
            print("Unknown command: {}".format(command_type))
        else:
            try:
                command[0] = self.model
                print(command_func(*command))
            except TypeError:
                print("Incorrect parameters number.")
                self.get_command_help(self.model, command_type)
            except Exception as e:
                print("Incorrect parameters format.")
                print(str(e))

    def add_all_commands(self):
        add = self.add_command
        add("help", self.get_command_help, "Prints command help.\n"
                                           "Format: <command>.\n"
                                           "'help all' returns general help")
        add("open", CM.open, "Reads the file for further modifications.\n"
                             "Format: <filename> "
                             "<optional: result_name>")
        add("path", CM.set_path, "Sets current path.\n"
                                 "Format: <path>")
        add("save", CM.save, "Saves track to file.\n"
                             "Format: <name> <filename>")
        add("rename", CM.rename_track, "Renames track.\n"
                                       "Format: <name> <new name>")
        add("close", CM.delete_track, "Deletes track from the list.\n"
                                      "Format: <name>")
        add("part", CM.part, "Gets part of track.\n"
                             "Format: <name> <start_time> "
                             "<finish_time> <optional: result_name>")
        add("join", CM.join, "Joins tracks.\n"
                             "Format: <name1> <name2> ...")
        add("insert", CM.insert, "Insert track in other track.\n"
                                 "Format: <base_track> <insert_track> "
                                 "<start_time> <optional: result_name>")
        add("delete", CM.delete, "Delete part of track.\n"
                                 "Format: <name> <start_time> "
                                 "<finish_time> "
                                 "<optional: result_name>")
        add("fade", CM.fade, "Fades track in or out.\n"
                             "Format: <in/out> <name> "
                             "<optional: result_name>")
        add("speed", CM.change_speed, "Changes speed of track.\n"
                                      "Format: <name> <ratio> "
                                      "<optional: result_name>")
        add("reverse", CM.reverse, "Reverses the track.\n"
                                   "Format: <name> <optional: result_name>")
        add("sum", CM.get_sum, "Gets sum of tracks.\n"
                               "Format: <name1> <name2> ...")
        add("volume", CM.change_loudness, "Changes volume level.\n"
                                          "Format: <name> <ratio> "
                                          "<optional: result_name>")
        add("compress", CM.compress, "Provides sound compression which "
                                     "is basically casting all the parts"
                                     "to the same volume level.\n"
                                     "Format: <name> <ratio> "
                                     "<optional: result_name>")
        add("list", CM.get_all_tracks_names, "Returns all the active tracks")
        add("exit", self.exit_program, "Exits the program.")

    def get_help(self):
        all_commands = ""
        for command, help_message in zip(self.command_helps.keys(),
                                         self.command_helps.values()):
            all_commands += "{}:\n{}\n\n".format(command, help_message)
        return ("Welcome to sound editor.\n\n"
                "Possible commands:\n" +
                all_commands)

    def get_command_help(self, console_model, command_type):
        if command_type == "all":
            return self.get_help()
        else:
            return self.command_helps[command_type]

    def exit_program(self, console_model):
        self.is_finished = True
        return "Bye bye"

    @staticmethod
    def parse_command(raw_command):
        by_quotes = raw_command.split('"')
        quoted_params = by_quotes[1::2]
        other_params = by_quotes[0::2]
        parsed_params = []
        for i in range(len(other_params)):
            cur_params = other_params[i].split(' ')
            cur_params = list(filter(lambda s: s != "", cur_params))
            parsed_params.extend(cur_params)
            if i < len(quoted_params):
                parsed_params.append(quoted_params[i])
        return parsed_params