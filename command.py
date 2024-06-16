#    DamienOS -- Shitty operating system (File:commands.py)
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

class CommandHandler:
	def __init__(self):
		self.KnownCommands = {}
		self.add_command(self.helpcommand, "Help", "<no arguments>", "Show system command help!", "Auto-updates")

	def add_command(self, function, name, args="", description="", notes="", pleaseNeeded=False):
		self.KnownCommands[name.lower()] = { # <== Capital letters in 'name' or the main command in the cli are ignored, unless they are arguments, at which point it is up to the command.
			"name": name,
			"command": function,
			"description": description,
			"args": args,
			"notes": notes
		}
		return 0

	def command(self, name="untitled", args="", description="", notes=""):
		"""Decorator for add_command()"""
		def decorator(function):
			self.add_command(function, name, args, description, notes)
			return function
		return decorator
		
	def run_command(self, command, i=False, please=False):
		"""Run a command!"""
		self.please = please
		cmd = command.split(" ")
		nocmd = False
		if all(char.isspace() for char in cmd[0]) or len(cmd) == 0:
			# blank command, do nothing.
			nocmd = True
			return 0
		cmd[0] = cmd[0].lower() # So that 'help', 'Help', 'HELP', and 'hELp' are the same.
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
					shared.logger.error("PLEASE password authentication has failed.")
					return
		if cmd[0].strip() == "#":
			return 0
#		print(nocmd)
		try:
			if (cmd[0] == "script") and (i == True):
				shared.logger.error("You cannot run a script from a script!")
				return 1
			s = self.KnownCommands[cmd[0]]["command"](self, cmd) # ==> It passes in the script name as well, just as sys.argv.
		except KeyError:
			shared.logger.error("?SYNTAX error?  The command \"{0}\" is not a command, operable program, or Holy-D script.".format(cmd[0]))
			return 1
		except Exception as e:
			# TODO fix migration to ctx/context systems.
			shared.logger.error("?FUNCTION error? The command \"{0}\" has encountered an error, so it cannot continue.".format(cmd[0]))
			shared.logger.error("==> This is NOT a problem with DamienOS, rather, it is an error in the command.  Error details are below.")
			errortype, msg, traceback = sys.exc_info()
			fname = os.path.split(traceback.tb_frame.f_code.co_filename)[1]
			#line = sys.exc_info[2].tb_lineno
			shared.logger.error("==> Error information")
			shared.logger.error("====> Error type: {0}".format(errortype))
			shared.logger.error("====> Error message: {0}".format(msg))
			shared.logger.error("====> Error line: {0}".format(traceback.tb_lineno))
			shared.logger.error("====> Error file: {0}".format(fname))
			return 1
		if s == None and system.data.get("main/display-noreturn-warning"):
			shared.logger.warn("This command did not return a exit code; it either returned None or")
			shared.logger.warn("ended without a return statement.")
			return 0
		else:
			if s != 0 and system.data.get("main/display-nonzero-warning") == True:
				shared.logger.warn("Script ended with a non-zero return code ({0}).".format(s))
				return

	# Help command -- it is the only command that is defined in this file/class.
	def helpcommand(self, ctx, args):
		t = PrettyTable()
		t.field_names = ["Command","Arguments","Description","Notes"]
		t.align["Description"] = "l"
		t.align["Notes"] = "l"
		for b in self.KnownCommands.keys():
			a = self.KnownCommands[b]
			t.add_row([a["name"],a["args"],a["description"],a["notes"]])
		print(t)
		return 0

def nocmd(ctx, args):
	pass
# make default instance.
handler = CommandHandler()

# [== add commands here ==]
# add_command(name, function, args="", description="", notes="")
# handler.add_command("Shell", commands.shell, "<none>", "Open the bash shell to do actually useful stuff.", notes="Exit to exit shell")
# handler.add_command("About", commands.about, "<none>", "Get DamienOS system information", notes="")
# handler.add_command("Script", script.holydscript, "<script>", "Run a Holy-D script!", "See documentation.")
# handler.add_command("ls", commands.ls, "<optional:directory>", "List files in the directory", "")
# handler.add_command("log", commands.log, "<type:info,warn,error,fatal,time>,[msg]", "Type MUST be valid")
# handler.add_command("mkdir", commands.mkdir, "<directory_name>", "Create a directory", "")
# handler.add_command("edit", commands.edit, "[file]", "Edit a file", "File can be blank")
# handler.add_command("Credits", commands.credits, "<none>", "Show the DamienOS credits", "")
# handler.add_command("echo", commands.echo, "[text]", "Echo text without fancy logging", "no color support")
# handler.add_command("cd", commands.cd, "[dir]", "Change the current working directory", "os.chdir(...)")
# handler.add_command("sleep", commands.sleep, "[time]", "Delay execution [time] seconds", "Must be int")
# handler.add_command("system", system.handler.system, "(see docs)", "Change system information", "You must use PLEASE")
# handler.add_command("please", lambda:nocmd, "<COMMAND>", "Privileged Level Execution Authorization and Security Escalation", "For please-enabled commands")
# handler.add_command("cowsay", commands.cowsay, "<text>", "cows are meant to talk", "")
# # handler.add_command("regview", commands.regview, "<key>", "Check registry value!")
# handler.add_command("registry", commands.registry, "[set,view]", "Registry commands")
# handler.add_command("rm", commands.rm, "[file]", "Delete a file!")
# handler.add_command("spinner", commands.spinner)