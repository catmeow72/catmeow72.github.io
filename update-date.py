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
notes_path = path.join(scriptdir, sys.argv[1])
found_frontmatter = False
found_date = False
with open(notes_path, "rt") as f:
    f.seek(0, os.SEEK_END)
    len = f.tell()
    f.seek(0, os.SEEK_SET)
    is_frontmatter = False
    before_frontmatter = True
    while f.tell() < len:
        line = f.readline()
        if before_frontmatter:
            pre += line
            if line.strip() == "---":
                before_frontmatter = False
                is_frontmatter = True
                found_frontmatter = True
        elif is_frontmatter:
            is_date = line.strip().startswith("date:")
            if line.strip() == "---":
                is_frontmatter = False
                if not found_date:
                    break
            else:
                if is_date:
                    found_date = True
            if not is_date:
                pre += line
            else:
                break
    post = f.read()
if not found_frontmatter:
    post = "---\n" + pre
    pre = "---\n"
with tempfile.NamedTemporaryFile(suffix=".md", mode="wt", delete_on_close=False, delete=False) as f:
    fpath = f.name
    f.write(pre)
    f.write("date: %s\n" % fmt)
    f.write(post)

os.rename(fpath, notes_path)
