#    DamienOS -- Shitty operating system (File:shared.py)
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

import termcolor
import os
import json
import sys
import log
from whiptail import Whiptail

global logger


SPINNER_FRAMES = ["-", "\\", "|", "/"]

logger = log.logger # im lazy lol
whiptail = Whiptail(title="DamienOS", backtitle="DamienOS build {}".format(open("/buildct","r").read().replace("\n","")))

def jsonLoad(f, fixData:dict=None, silent=False):
	logger.info("Beginning load of JSON file <{0}>".format(f), silent=silent)
	logger.info("....Beginning pre-load of file", silent=silent)
	if os.path.isfile(f) == False:
		logger.error("........File does not exist :(", silent=silent)
		if fixData == None:
			logger.fatal("........Exiting, error is not recoverable.  I DONT WANNA DIE!", silent=silent)
			raise FileNotFoundError("aint not existing :/")
		logger.warn("............Beginning auto-fix attempt", silent=silent)
		presubstep = logger.sstep
		_curstep = logger.cstep
		_substep = logger.sstep
		logger.step("Fix broken JSON file", silent=silent)
		logger.substep("Diagnose error", silent=silent)
		logger.warn("............Diagnosing error", silent=silent)
		if os.path.isfile(f) == False:
			logger.warn("................The file does not exist", silent=silent)
		logger.substep("Fixing file")
		logger.warn("............Recreating the file as it is broken or does not exist.", silent=silent)
		with open(f, "w") as _f:
			json.dump(fixData, _f)
		logger.substep("All done", silent=silent)
		logger.step(_curstep)
		logger.substep(_substep)
		logger.warn("................All done!  Returning to normal execution!", silent=silent)
	fi = open(f, "r")
	logger.info("........Pre-load successful", silent=silent)
	logger.info("....Loading file", silent=silent)
	j = json.load(fi)
	logger.info("....Load OK, no errors found.", silent=silent)
	return j


def chdir(dir):
	os.chdir(dir)
	logger.info("Selected previously unselected directory <{0}>".format(dir))

def nocommand(*, f) -> Exception:
	logger.error("This command has not been implemented; It exists only as a placeholder.")
	return Exception


