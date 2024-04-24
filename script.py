#    DamienOS -- Shitty operating system (File:script.py)
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
import os

def holydscript(ctx, args):
	"""Run Holy-D script
	@args <script>"""
	if len(args) == 1:
		shared.logger.error("No script given!")
		shared.logger.error("Usage: script <scriptpath>")
		return 1
	if os.path.isfile(args[1]) == False:
		shared.logger.error("Script given does not exist!")
		shared.logger.error("Usage: script <scriptpath>")
		return 1
	sl = [l.replace("\n", "") for l in open(args[1], "r").readlines() if "??" not in l]

	if len(sl) < 1:
		shared.logger.error("Script seems to be empty (Lines < 1)")
		return

	for l in sl:
		rs = r.split(" ")
		if len(rs) > 0:
			rs[0] = rs[0].lower()
			if rs[0] == "ret":
				try:
					ret = int(rs[1])
					return ret
				except ValueError:
					shared.logger.error("Script must end with a integer")
					return 1
		r = ctx.run_command(l, i=True)
		if r == 1:
			shared.logger.error("==> There is an error in this script, so it will stop.")
			return
		return 0
	print("==> SCRIPT EXITED")
