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
import system
import shutil


@handler.command("shell", "Opens the BASH shell", "for when you want to do useful stuff lol", alias=["sh"])
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

    if not os.path.isdir(dir):
        shared.logger.error("Directory \"%s\" doesn't exist!" % dir)
        return 1
    l = os.listdir(dir)
    print("Total %s" % len(l))
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

    _args = args[:]
    del _args[0]
    for entry in _args:
        if entry == "":
            continue
        if os.path.isdir(entry):
            print("Directory %s already exists, skipping it." % entry)
            continue
        os.mkdir(entry)
        if system.data.get("main/display-verbose-output"):
            print("Created directory %s" % entry)

    return 0


@handler.command("log", "<type:info,warn,error,fatal,time> [message]", "Logs with special formatting")
def log(ctx, args):
    """Send a logging message to STDOUT.
    @args <type> message"""
    if len(args) < 3:  # 2 or less
        shared.logger.error("Invalid syntax.")
        shared.logger.error(
            "Usage: log <level:info,warn,error,fatal,time> [ text ]")
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


@handler.command("edit", "[file]", "Literally the nano editor", alias=["nano"])
def edit(ctx, args):
    if len(args) < 2:
        file = ""
    else:
        file = args[1]
    subprocess.call("$(which nano) {}".format(file), shell=True)
    return 0


@handler.command("remove", "[files]", "Remove some files", alias=["rm"])
def remove(ctx, args):
    if len(args) < 2:
        shared.logger.error("One or more files must be specified.")
        return 1

    _args = args[:]
    del _args[0]
    for entry in _args:
        if os.path.isdir(entry):
            try:
                os.removedirs(entry)
                if system.data.get("main/display-verbose-output"):
                    print("Removed directory %s" % entry)
            except OSError:
                print("%s: Directory not empty" % entry)
                continue
        elif os.path.isfile(entry):
            os.remove(entry)
            if system.data.get("main/display-verbose-output"):
                print("Removed regular file %s" % entry)
        else:
            print("%s does not exist." % entry)
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
        shared.logger.error(
            "cd: The directory '{}' does not exist!".format(args[1]))
        return 1
    except NotADirectoryError:
        shared.logger.error("cd: '{}' is not a directory!".format(args[1]))
        return 1
    return 0


@handler.command("catalog", "[file]", "(cat) read a file", alias=["cat"])
def catalog(ctx, args):
    if len(args) < 2:
        shared.logger.error("Usage: catalog [file]")
        return 1

    if not os.path.isfile(args[1]):
        shared.logger.error("File %s does not exist." % args[1])
        return 1

    with open(args[1]) as f:
        print(f.read())
        return 0


@handler.command("about", "(no arguments)", "About AlphaOS and legal mumbo jumbo")
def about(ctx, args):
    PREF, CODE = shared.whiptail.menu("Please select an option to learn more about AlphaOS.", [
        "How it Was Made",
        "Credits",
        "Legal Disclaimer",
        "License",
        "Exit"
    ])
    if system.data.get("main/display-verbose-output"):
        print("verbose: Recieved message preference: \"{0}\", and recieved Whiptail code {1}.".format(
            PREF, CODE))
    if PREF == "How it Was Made":
        shared.whiptail.textbox("/docker/documents/HOW_IT_WAS_MADE.txt")
        return about(ctx, args)
    if PREF == "Credits":
        shared.whiptail.textbox("/docker/documents/CREDITS.txt")
        return about(ctx, args)
    elif PREF == "Legal Disclaimer":
        shared.whiptail.textbox("/docker/documents/ALPHAOS_DISCLAIMER.txt")
    elif PREF == "License":
        shared.whiptail.textbox("/docker/documents/LICENSE.txt")
        return about(ctx, args)
    elif PREF == "Exit":
        return 0
    return 1


@handler.command("whoami", "(no arguments)", "Just to help if you're having an identity crisis :)")
def whoami(ctx, args):
    print(system.data.get("main/username"))
    return 0


@handler.command("pwd", "(no arguments)", "Get your current working directory")
def cwd(ctx, args):
    print(os.getcwd())
    return 0


@handler.command("copy", "[from] [to]", "Copy a file!", alias=["cp"])
def copy(ctx, args):
    _a = args[:]
    del _a[0]
    if len(args) < 2:
        shared.logger.error("Usage: copy [source/from] [dist/to]")
        return 1
    if not os.path.isfile(_a[0]):
        shared.logger.error("Source file \"%s\" doesn't exist!" % _a[0])
        return 1
    shutil.copy(_a[0], _a[1])
    if system.data.get("main/display-verbose-output"):
        print("Copied \"%s\" to \"%s\"." % (_a[0], _a[1]))
    return 0


@handler.command("whereis", "[command]", "Show the qualified name of a command", alias=["which"])
def whereis(ctx, args):
    # oh hey a command that actually uses ctx
    if len(args) < 2:
        shared.logger.error("Usage: whereis [command]")
        return 1
    try:
        c = ctx.KnownCommands[args[1]]
    except ValueError:
        shared.logger.error("Not a valid command.")
        return 1
    o = ""
    if c["type"] == "alias":
        if system.data.get("main/display-verbose-output"):
            print("verbose: This is a alias to \'%s\'!" % c["target"])

        o = o + "%s -> " % args[1]

        c = ctx.KnownCommands[c["target"]]

    o = o + "%s -> %s" % (c["name"], c["command"].__name__)

    print(o)
    return 0


@handler.command("touch" "[file]", "Create a blank file")
def touch(ctx, args):
    pass


@handler.command("python", "[code]", "run python code as alphaos")
def _handle_python_eval(ctx, args):
    if len(args) > 1:
        _ = args[:]
        del _[0]
        cmd = " ".join(_)

        try:
            exec(cmd)
        except Exception as e:
            print("%s: %s" % (type(e).__name__, repr(e)))
        return
    cmd = ""

    pr = ""
    print("Entering Python console.  Enter 'run' to run this code and exit.")
    while pr.lower().strip() != "run":
        pr = input("python >>> ")

        if pr.lower().strip() == "run":
            break

        cmd = cmd + pr + "\n"
    return exec(pr)
