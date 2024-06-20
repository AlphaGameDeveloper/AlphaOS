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

from command import handler
import subprocess
import os
import shared
import termcolor
@handler.command("shell", "Opens the BASH shell", "for when you want to do useful stuff lol")
def shell(ctx, args=None):
	"""Open BASH shell command
	@args none"""
	print("==> Opening bash shell; Type 'exit' to exit the shell.")
	subprocess.call("/bin/bash", shell=True)
	print("==> Returning to DamienOS")
	return 0

@handler.command("ls", "<dir>", "List a directory")
def ls(ctx, args):
	if len(args) < 2:
		dir = "."
	else:
		dir = args[1]

	l = os.listdir(dir)
	for i in l:
		if os.path.isfile(i):
			print("[FILE]  {0}".format(i))
		else:
			print("[{0}]  {1}".format(termcolor.colored(" DIR", "blue"), i))
	return 0

@handler.command("mkdir", "[directory]", "Creates a directory")
def mkdir(ctx, args):
	if len(args) < 2:
		shared.logger.error("You need to give a directory name!")
		shared.logger.error("Usage: mkdir <directory_name>")
		return
	subprocess.call(["mkdir", args[1]])
	return 0

@handler.command("log", "<type:info,warn,error,fatal,time> [message]", "Logs with special formatting")
def log(ctx, args):
	"""Send a logging message to STDOUT.
	@args <type> message"""
	if len(args) < 3: # 2 or less
		shared.logger.error("Invalid syntax.")
		shared.logger.error("Usage: log <level:info,warn,error,fatal,time> [ text ]")
		return 1
	args[1] = args[1].lower()
	_t = args[:]
	del _t[1]
	del _t[0]
	if args[1] == "info":
		shared.logger.info(" ".join(_t))
	elif args[1] == "warn":
		shared.logger.warn(" ".join(_t))
	elif args[1] == "error":
		shared.logger.error(" ".join(_t))
	elif args[1] == "fatal":
		shared.logger.fatal(" ".join(_t))
	elif args[1] == "time":
		shared.logger.time(" ".join(_t))
	else:
		shared.logger.error("Invalid log type: {0}".format(args[1]))
		return 1
	return 0

@handler.command("edit", "[file]", "Literally the nano editor")
def edit(ctx, args):
	if len(args) < 2:
		file = ""
	else:
		file = args[1]
	subprocess.call("/bin/nano {}".format(file), shell=True)
	return 0

@handler.command("echo", "[text]", "Echo text without extra formatting")
def echo(ctx, args):
	del args[0]
	print(" ".join(args))
	return 0

@handler.command("cd", "[directory]", "Change Directory")
def cd(ctx, args):
	if len(args) < 2:
		return
	try:
		os.chdir(args[1])
	except FileNotFoundError:
		shared.logger.error("cd: The directory '{}' does not exist!".format(args[1]))
		return 1
	except NotADirectoryError:
		shared.logger.error("cd: '{}' is not a directory!".format(args[1]))
		return 1
	return 0
