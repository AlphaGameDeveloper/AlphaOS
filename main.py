#    DamienOS -- Shitty operating system
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
print("[INIT]  Loading libraries - Please wait.")
import termcolor
import json
import os
import sys
import time
import subprocess
import command
import shared
import system
#from whiptail import Whiptail

global logger
logger = None

def boot():
	print("[INIT]  Beginning logging services.")
	global logger
	logger = shared.logger
#	print(logger)
	logger.info("Done starting logging services!")
	logger.step("Main boot system")
	shared.chdir("/data")
	logger.substep("Load JSON files and parse settings")
	cfg = shared.jsonLoad("/data/system-settings.json", fixData={"fix": True})
	logger.step("Boot")
	logger.substep("Opening terminal and accept user input")
	logger.info("+----------------------------------------+")
	logger.info("|             DamienOS build             |")
	logger.info("+----------------------------------------+")
	logger.info("| 01 BUILD     : {0}".format(system.data.get("build/number")))
	logger.info("| 02 BUILDTIME : {0}".format(system.data.get("build/time")))
	logger.info("| 03 LICENSE   : GPL-3-OR-LATER")
	logger.info("+----------------------------------------+")
	logger.step("Start")
	logger.substep("Start DamienOS main interactive mode")

def cli():
	print(open("/docker/banner.txt", "r").read())
	#username = "damienos" if not os.getenv("USERNAME") else os.getenv("USERNAME")
	if system.data.get("main/password-sha256") == "6b3a55e0261b0304143f805a24924d0c1c44524821305f31d9277843b8a10f4e":
		# password = 'password'
		shared.logger.warn("==> WARNING: PASSWORD IS SET TO DEFAULT!  DO 'please passwd' TO CHANGE IT!")
		shared.logger.warn("====> Password = 'password'")
	while True:
		username = system.data.get("main/username")
		dir = os.getcwd()
		cmd = input("{0}> [{1}] -->".format(termcolor.colored(username, "red"), termcolor.colored(("~" if dir == "/data" else dir), "blue")))
		try:
			command.handler.run_command(cmd)
		except Exception as e:
			shared.logger.error("Error! Type={}".format(
							type(e).__name__))
			for i in range(5):
				sys.stdout.write("\rRecovering from fatal error.   ETA={}".format(i+1))
				time.sleep(1)
			sys.stdout.write("\n")
			shared.logger.info("Saved traceback... Save successful.")
			shared.logger.warn("Internal error hash SHA256: {}".format(hash(e)))



	debug = (True if os.getenv("DEBUG") else False)
	if debug:
		exec("."*50)
		_time("Query {0}; Time={1}s".format(("OK" if ok == True else "NOT OK"), time.perf_counter() - start_time))

def pinkScreenGUI():
	shared.whiptail.msgbox("""              _
             / )
         _  / /       Well, this is awkward!
        (_)( (          AlphaOS crashed against a wall and can't get back up :/
           | |          AlphaOS will now restart, to clean myself up.
         _ ( (
        (_) \ \\  Please make a GitHub issue, that would help loads!
             \_)
""")

def begin():
	try:
		boot()
		cli()
	except KeyboardInterrupt:
		pinkScreenGUI()
		begin()

begin()
