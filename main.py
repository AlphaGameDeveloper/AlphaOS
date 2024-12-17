#    AlphaOS -- Shitty operating system
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
import commands.www
import commands.basic_utility
import commands.commands
import command
import subprocess
import readline
import time
import sys
import os
import json
import termcolor
import system
import shared
import error
print("[INIT]  Loading libraries - Please wait.")
shared.setSystem(system)


# from whiptail import Whiptail

global logger
logger = None


def boot():
    print("[INIT]  Beginning logging services.")
    global logger
    logger = shared.logger
# print(logger)
    logger.info("Done starting logging services!")
    logger.step("Main boot system")
    shared.chdir("/data")
    logger.substep("Load JSON files and parse settings")
    # cfg = shared.jsonLoad("/data/system-settings.json", fixData={"fix": True})
    logger.step("Boot")
    logger.substep("Opening terminal and accept user input")
    logger.info("+---------------------------------------+")
    logger.info("|             AlphaOS build             |")
    logger.info("+---------------------------------------+")
    logger.info("| 01 BUILD     : {0}".format(system.data.get("build/number")))
    logger.info("| 02 BUILDTIME : {0}".format(system.data.get("build/time")))
    logger.info("| 03 LICENSE   : GPL-3-OR-LATER")
    logger.info("+---------------------------------------+")
    logger.step("Start")
    logger.substep("Start AlphaOS main interactive mode")


def cli():
    if system.data.get("main/banner/enabled"):
        banner_location = system.data.get("main/banner/location")
        if os.path.isfile(banner_location):
            with open(banner_location, "r") as f:
                print(f.read())
        else:
            shared.logger.error("Cannot find the banner file!  Modify the location by changing the")
            shared.logger.error("main/banner/location registry key, or disable it by turning off main/banner/enabled!")
    # username = "AlphaOS" if not os.getenv("USERNAME") else os.getenv("USERNAME")
    if system.data.get("main/password-sha256") == "6b3a55e0261b0304143f805a24924d0c1c44524821305f31d9277843b8a10f4e":
        # password = 'password'
        shared.logger.warn(
            "==> WARNING: PASSWORD IS SET TO DEFAULT!  DO 'please passwd' TO CHANGE IT!")
        shared.logger.warn("====> Password = 'password'")
    while True:
        ok = True
        blank = False
        username = system.data.get("main/username")
        dir = os.getcwd()
        try:
            cmd = input("{0}> [{1}] -->".format(termcolor.colored(username, "red"),
                        termcolor.colored(("~" if dir == "/data" else dir), "blue")))
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            continue
        if cmd.strip() == "":
            blank = True

        try:
            start_time = time.perf_counter()
            command.handler.run_command(cmd)
            ok = True
        except Exception as e:
            ok = False
            shared.logger.error(repr(e))

        if system.data.get("main/display-postcommand-summary") and not blank:
            shared.logger.exec("."*50)
            shared.logger.exec("Query {0}; Time={1}ms".format(
                ("OK" if ok == True else "NOT OK"), round((time.perf_counter() - start_time)*10, 2)))


def pinkScreenGUI(e):
    error.ErrorHandler(e).callPinkScreen()


def begin():
    try:
        boot()
        cli()
    except Exception as e:
        shared.logger.error("FATAL ERROR: {0}".format(repr(e)))
        pinkScreenGUI(e)


if __name__ == "__main__":
    shared.logger.step("Legal Disclaimer")
    shared.logger.substep("Show AlphaOS Legal Disclaimer")
    shared.logger.info("Showing AlphaOS Legal Disclaimer.")
    _ = shared.whiptail.textbox("/docker/documents/ALPHAOS_DISCLAIMER.txt")

    g = shared.whiptail.yesno("Do you accept the terms and conditions?")

    shared.logger.info("Legal Disclaimer shown, got {}.".format(g))

    if not g:
        shared.whiptail.msgbox("Legal Disclaimer denied.  Exiting.")
        exit(1)

    shared.logger.substep("All Done")
    shared.logger.step("Starting begin process")
    begin()
