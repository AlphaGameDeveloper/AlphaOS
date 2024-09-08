#    AlphaOS -- Shitty operating system (file:error.py)
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
import system
import sys
import traceback

class ErrorHandler:
    def __init__(self, error: Exception):
        self.ERROR = error

    def callPinkScreen(self):
        option = shared.whiptail.menu("AlphaOS has encountered a severe error and cannot contiue.", items=("Exit", "See Error Information"))[0]

        shared.logger.info("PinkScreen shown, got %s" % str(option))   

        if option == "Exit":
            sys.exit(1)
        elif option == "See Error Information":
            return self.seeErrorInformation()
        else:
            shared.logger.error("Invalid option \"%s\".  Exiting." % option)
            sys.exit(1)
            
    def seeErrorInformation(self):
        tb = traceback.format_tb(self.ERROR.__traceback__)
        shared.whiptail.msgbox("Error: %s\n\n\n-- TRACEBACK --\n%s" % (repr(self.ERROR), "\n".join(tb)))
        return self.callPinkScreen()