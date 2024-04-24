#    DamienOS -- Shitty operating system (file:extentions.py)
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

# --- required imports -- do not touch! ---
import shared
# --- END required imports ---
# --- extensions imports ---

# ---

class ExtensionManager:
	def __init__(self):
		self.modules = []

	def add_extension_pack(self, module)
		self.modules.append([{
			"module-name": module.METADATA["name"],
			"registered_commands": [{
				"name": c["name"],
				"function": c["function"],
				"description": c["description"],
				"args": c["args"],
				"notes": c["notes"]} for c in module.METADATA["commands"])

manager = ExtensionManager()

# --- Call manager.add_extension_pack here ---

# ------

# EOF

