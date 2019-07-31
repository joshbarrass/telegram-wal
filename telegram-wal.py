#!/usr/bin/env python2

## Telegram-Wal
# Generate telegram theme based on pywal colours

import sys
import cmdarg
from cmdarg import TooManyArgs, NotEnoughArgs
import subprocess
from PIL import Image
from zipfile import ZipFile
import os

MINARGS = 1
MAXARGS = 1
THEME_EXT = "cnf"

if not sys.modules.has_key("idlelib"):
    try:
        args = cmdarg.get_arg_dict(MINARGS,MAXARGS)
    except TooManyArgs:
        print "Too many arguments: Telegram-Wal takes at most {m} args.".format(m=MAXARGS)
        raise
    except NotEnoughArgs:
        print "Not enough arguments: Telegram-Wal takes at least {m} args.".format(m=MINARGS)
        raise
else:
    args = {0:sys.argv[0],1:"test"}

theme = "default"
if args.has_key("t"):
    theme = args["t"]
elif args.has_key("theme"):
    theme = args["theme"]

external_colours = None
if "x" in args:
    external_colours = args["x"]
elif "external-colors" in args:
    external_colours = args["external-colors"]


p = subprocess.Popen(["xrdb","-query"], stdout=subprocess.PIPE)
Xvars, err = p.communicate()
Xvars = dict([keypair.strip("*").split("\t") for keypair in Xvars.replace(":","").strip("\n").split("\n") if keypair[0] == "*"])

COLORS = {"color0": Xvars[".color0"],
          "color1": Xvars[".color1"],
          "color2": Xvars[".color2"],
          "color3": Xvars[".color3"],
          "color4": Xvars[".color4"],
          "color5": Xvars[".color5"],
          "color6": Xvars[".color6"],
          "color7": Xvars[".color7"],
          "color8": Xvars[".color8"],
          "color9": Xvars[".color9"],
          "color10": Xvars[".color10"],
          "color11": Xvars[".color11"],
          "color12": Xvars[".color12"],
          "color13": Xvars[".color13"],
          "color14": Xvars[".color14"],
          "color15": Xvars[".color15"],
          "background": Xvars[".background"],
          "foreground": Xvars[".foreground"]}

if external_colours is None:
    theme = open("themes/{theme}.{ext}".format(theme=theme, ext=THEME_EXT))
    raw_theme = theme.read()
    theme.close()
    
    formatted_theme = raw_theme.format(**COLORS)
else:
    with open(external_colours) as f:
        formatted_theme = f.read()

output_fn = "/tmp/colors.tdesktop-palette"

output_file = open(output_fn, "w")
output_file.write(formatted_theme)
output_file.close()

output_image = "/tmp/background.png"
im = Image.new("RGB", (100, 100), COLORS["background"])
im.save(output_image)

output_theme = args[1] + ".tdesktop-theme"
with ZipFile(output_theme, "w") as zf:
    zf.write(output_fn, arcname=os.path.split(output_fn)[-1])
    os.remove(output_fn)
    zf.write(output_image, arcname=os.path.split(output_image)[-1])
    os.remove(output_image)
