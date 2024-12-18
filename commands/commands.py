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

import cowsay as _cowsay
import subprocess
from prettytable import PrettyTable
import shared
import os
import termcolor
import time
import whiptail
import sys
import system
from command import handler


@handler.command("sleep", "Sleep for a specified amount of time")
def sleep(ctx, args):
    if len(args) < 2:
        shared.logger.error("No time specified")
        shared.logger.error("Usage: sleep <time>")
        return 1
    try:
        time.sleep(float(args[1]))
    except ValueError:
        shared.logger.error(
            "Integer value needed for sleep.  Value is NaN or a float.")
        return 1
    return 0


@handler.command("cowsay", "The traditional cowsay command from Linux!")
def cowsay(ctx, args):
    if len(args) < 2:
        shared.logger.error("Usage: cowsay <text>")
        return 1
    a = args[:]
    del a[0]
    r = " ".join(a)
    _cowsay.cow(r)
    return 0


@handler.command("registry", "View and set system registry values")
def registry(ctx, args) -> int:
    if len(args) < 2:
        shared.logger.error("No subcommand given!")
        shared.logger.error("Valid subcommands are:")
        shared.logger.error("  - view (view a registry value)")
        shared.logger.error("  - set (set a registry value)")
        shared.logger.error("  - reload (reload the registry)")
        return 0

    subcommand = args[1].lower()

    if subcommand == "view" or subcommand == "get":
        if len(args) < 3:
            shared.logger.error("You need to give a registry path!")
            shared.logger.error("Usage: registry view (path)")
            return 0

        try:
            d = system.data.get(args[2])
        except Exception as e:
            print("Cannot get registry: %s" % repr(e))
            return 1
        if isinstance(d, dict):
            print("Dictionary Content")
            for entry in d.keys():
                ty = type(d[entry]).__name__
                print("- %s (Type: %s)" % (entry, ty))
        elif isinstance(d, list):
            print("List Content")
            for entry in d:
                print("- %s" % entry)

        else:
            print(d)

        return 0

    elif subcommand == "reload":
        system.data.reload(quiet=True)
        shared.logger.info("System registry reloaded!")

    elif subcommand == "set":
        if len(args) < 4:
            shared.logger.error("You need to give a registry path and value!")
            shared.logger.error("Usage: registry set (path) (value)")
            return 0
        value = args[3]
        if value.lower() == "true" or value.lower() == "True":
            value = True
        elif value.lower() == "false" or value.lower() == "False":
            value = False
        else:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
        system.data.set(args[2], value)

        shared.logger.info("Registry value set!")
        return 0
    else:
        shared.logger.error("Invalid subcommand!")
        return 1


def rm(ctx, args):
    if len(args) < 2:
        shared.logger.error("Need a file path to delete!")
        shared.logger.error("Usage: rm <file>")
        return 1
    if os.path.isfile(args[1]):
        os.remove(args[1])
        return 0
    else:
        shared.logger.error("Sorry, but that file doesn't exist...")
        return 1


@handler.command("spinner")
def spinner(ctx, args):
    while True:
        for frame in shared.SPINNER_FRAMES:
            sys.stdout.write("\r%s" % frame)
            time.sleep(.1)
