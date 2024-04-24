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

global _info
global _error
global _warn
global _fatal
global _exec
global __time
global logger

logger = log.logger # im lazy lol
whiptail = Whiptail(title="DamienOS", backtitle="DamienOS build {}".format(open("/buildct","r").read().replace("\n","")))
_info, _error, _warn, _fatal, _exec, __time = 0, 0, 0, 0, 0, 0

def jsonLoad(f, fixData:dict=None):
	logger.info("Beginning load of JSON file <{0}>".format(f))
	logger.info("....Beginning pre-load of file")
	if os.path.isfile(f) == False:
		logger.error("........File does not exist :(")
		if fixData == None:
			logger.fatal("........Exiting, error is not recoverable.  I DONT WANNA DIE!")
			raise FileNotFoundError("aint not existing :/")
		logger.warn("............Beginning auto-fix attempt")
		presubstep = logger.sstep
		_curstep = logger.cstep
		_substep = logger.sstep
		logger.step("Fix broken JSON file")
		logger.substep("Diagnose error")
		logger.warn("............Diagnosing error")
		if os.path.isfile(f) == False:
			logger.warn("................The file does not exist")
		logger.substep("Fixing file")
		logger.warn("............Recreating the file as it is broken or does not exist.")
		with open(f, "w") as _f:
			json.dump(fixData, _f)
		logger.substep("All done")
		logger.step(_curstep)
		logger.substep(_substep)
		logger.warn("................All done!  Returning to normal execution!")
	fi = open(f, "r")
	logger.info("........Pre-load successful")
	logger.info("....Loading file")
	j = json.load(fi)
	logger.info("....Load OK, no errors found.")
	return j


def chdir(dir):
	os.chdir(dir)
	logger.info("Selected previously unselected directory <{0}>".format(dir))

def nocommand(*, f) -> Exception:
	logger.error("This command has not been implemented; It exists only as a placeholder.")
	return Exception


