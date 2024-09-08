#    AlphaOS -- Shitty operating system (File:commands.py)
#    Copyright (C) 2023  Damien Boisvert (AlphaGameDeveloper)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import shared
from prettytable import PrettyTable
import time
import sys
import script
import os
import system
import please
import termcolor

class CommandHandler:
    def __init__(self):
        self.KnownCommands = {}
        self.add_command(self.helpcommand, "Help", "<no arguments>",
                         "Show system command help!", "Auto-updates")

    def add_command(self, function, name, args="", description="", notes="", alias=[], pleaseNeeded=False):
        self.KnownCommands[name.lower()] = {  # <== Capital letters in 'name' or the main command in the cli are ignored, unless they are arguments, at which point it is up to the command.
            "type": "command",
            "name": name,
            "command": function,
            "description": description,
            "args": args,
            "notes": notes,
            "alias": alias
        }
        for a in alias:
            self.KnownCommands[a.lower()] = {
                "type": "alias",
                "target": name.lower()
            }
        return 0

    def command(self, name="untitled", args="", description="", notes="", alias=[]):
        """Decorator for add_command()"""
        def decorator(function):
            self.add_command(function, name, args, description, notes, alias)
            return function
        return decorator

    def run_command(self, command, inScript=False, please=False):
        """Run a command!"""
        self.please = please
        cmd = command.split(" ")
        nocmd = False
        if all(char.isspace() for char in cmd[0]) or len(cmd) == 0:
            # blank command, do nothing.
            nocmd = True
            return 0
        # So that 'help', 'Help', 'HELP', and 'hELp' are the same.
        cmd[0] = cmd[0].lower()
        if cmd[0] == "exit":
            shared.logger.exec("Goodbye")
            shared.logger.exec("Logout complete at <{0}>".format(time.ctime()))
            sys.exit(0)
        if cmd[0] == "please":
            please.attempt()
            with open("/.please-attempt", "rb") as f:
                if f.read() == bytes(system.data.get("main/password-sha256"), 'utf-8'):
                    del cmd[0]
                    self.run_command(" ".join(cmd), please=False)
                else:
                    shared.logger.error(
                        "PLEASE password authentication has failed.")
                    return
        if cmd[0].strip() == "#":
            return 0
# print(nocmd)
        try:
            if (cmd[0] == "script") and (inScript == True):
                shared.logger.error("You cannot run a script from a script!")
                return 1
            target = self.KnownCommands[cmd[0]]
            if target["type"] == "alias":
                target = self.KnownCommands[target["target"]]
            s = target["command"]
        except KeyError:
            aliases = system.data.get("alias/aliases")
            if cmd[0] in aliases.keys():
                cmd_ = cmd[0]
                cmd_args = cmd[1:]
                sh_command = "%s%s" % (aliases[cmd_]["command"], 
                                (" " + " ".join(cmd_args) if system.data.get(f"alias/aliases/{cmd_}/append-arguments") else ""))
                print("'%s'" % sh_command)
                s = lambda ctx, args: os.system(sh_command)
            else:
                shared.logger.error(
                    "?SYNTAX error?  The command {0} is not a command, operable program, or Holy-D script.".format(
                        termcolor.colored("\"%s\"" % cmd[0], "blue", attrs=["bold"])))
                    
                return 1

        try:
            # run it
            command_result = s(self, cmd)
        except KeyboardInterrupt:
            sys.stdout.write("^C\n")
            command_result = 255 # keyboard interrupt
        except Exception as e:
            # TODO fix migration to ctx/context systems.
            shared.logger.error(
                "?FUNCTION error? The command \"{0}\" has encountered an error, so it cannot continue.".format(cmd[0]))
            shared.logger.error(
                "==> This is NOT a problem with AlphaOS, rather, it is an error in the command.  Error details are below.")
            errortype, msg, traceback = sys.exc_info()
            fname = os.path.split(traceback.tb_frame.f_code.co_filename)[1]
            # line = sys.exc_info[2].tb_lineno
            shared.logger.error("==> Error information")
            shared.logger.error("====> Error type: {0}".format(errortype))
            shared.logger.error("====> Error message: {0}".format(msg))
            shared.logger.error(
                "====> Error line: {0}".format(traceback.tb_lineno))
            shared.logger.error("====> Error file: {0}".format(fname))
            return 1
        if command_result == None and system.data.get("main/display-noreturn-warning"):
            shared.logger.warn(
                "This command did not return a exit code; it either returned None or")
            shared.logger.warn("ended without a return statement.")
            return 0
        else:
            if command_result != 0 and system.data.get("main/display-nonzero-warning") == True:
                shared.logger.warn(
                    "Script ended with a non-zero return code ({0}).".format(command_result))
                return

    # Help command -- it is the only command that is defined in this file/class.
    def helpcommand(self, ctx, args):
        t = PrettyTable()
        t.field_names = ["Command", "Arguments",
                         "Description", "Notes", "Aliases"]
        t.align["Description"] = "l"
        t.align["Notes"] = "l"
        for b in self.KnownCommands.keys():
            a = self.KnownCommands[b]
            if a["type"] == "alias":
                continue  # alias will not be put in it's own row!

            t.add_row([a["name"], a["args"], a["description"],
                      a["notes"], ", ".join(a["alias"])])
        print(t)
        return 0


# make default instance.
handler = CommandHandler()
