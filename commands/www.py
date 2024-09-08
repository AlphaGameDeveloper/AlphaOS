#    AlphaOS -- Shitty operating system (File:commands/www.py)
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
import wget as _wget  # to avoid conflict with command with the same name
import shared
import os


@handler.command("wget", "[url]", "Download file at specified URL", "Scuffed AF")
def wget(ctx, args):
    if len(args) < 3:
        shared.logger.error("Usage: wget [url] [output]")
        return 1

    fn = _wget.download(args[1], out=args[2])
    print(fn)


@handler.command("curl", "[url] (curl opts)", "cURL command-line utility")
def curl(ctx, args):
    _a = args[:]
    del _a[0]
    os.system("curl %s" % " ".join(_a))
    return 0


@handler.command("lynx", "[url] (lynx args)", "Lynx in-terminal Web Browser!")
def lynx(ctx, args):
    _a = args[:]
    del _a[0]
    os.system("lynx %s" % " ".join(_a))
    return 0
