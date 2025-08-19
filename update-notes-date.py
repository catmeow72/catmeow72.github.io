#!/usr/bin/env python3
import os
import sys
from os import path
import tempfile
from datetime import datetime, timezone, timedelta
from subprocess import run
scriptdir = path.realpath(path.dirname(__file__))
curtime = datetime.now(timezone.utc).astimezone()
fmt = curtime.strftime("%Y-%m-%d %H:%M:%S ")
utc_offset = curtime.utcoffset()
if utc_offset != None:
    offs = utc_offset / timedelta(minutes=1)
else:
    print("Error: Failed to get UTC offset!")
    sys.exit(1)
offs_abs = abs(offs)
sign = offs / offs_abs
while offs_abs > 60 * 24:
    offs_abs -= 60 * 24
    sign *= -1
fmt += "+" if sign >= 0 else "-"
fmt += "%02d%02d" % (offs_abs // 60, offs_abs % 60)
pre = ""
post = ""
notes_path = path.join(scriptdir, "notes.md")
with open(notes_path, "rt") as f:
    f.seek(0, os.SEEK_END)
    len = f.tell()
    f.seek(0, os.SEEK_SET)
    is_frontmatter = False
    date_found = False
    before_frontmatter = True
    while f.tell() < len:
        line = f.readline()
        if before_frontmatter:
            pre += line
            if line.strip() == "---":
                before_frontmatter = False
                is_frontmatter = True
        elif is_frontmatter:
            is_date = line.strip().startswith("date:")
            if line.strip() == "---":
                is_frontmatter = False
            else:
                if is_date:
                    date_found = True
            if not is_date:
                pre += line
            else:
                break
    post = f.read()
with tempfile.NamedTemporaryFile(suffix=".md", mode="wt", delete_on_close=False, delete=False) as f:
    fpath = f.name
    f.write(pre)
    f.write("date: %s\n" % fmt)
    f.write(post)

editor = os.environ.get("EDITOR")
if editor == None:
    editor = "vim"
def prompt(text: str = "", default: bool =True) -> bool:
    resp: bool|None = None
    printed_error: bool = False
    while resp == None:
        resp_str: str = input(text + " [%s] " % ("Y/n" if default else "y/N")).casefold()
        if resp_str == "":
            resp = default
        elif resp == "no".casefold() or resp_str == "n".casefold():
            resp = False
        elif resp == "yes".casefold() or resp_str == "y".casefold():
            resp = True
        elif not printed_error:
            print("\x1b[1A\r\x1b[0KPlease type 'yes' or 'no'.")
            printed_error = True
    return resp
if prompt("Would you like to view and/or edit the new contents now?", True):
    run([editor, fpath])
if prompt("Keep the file?", True):
    os.rename(fpath, notes_path)
else:
    os.remove(fpath)
