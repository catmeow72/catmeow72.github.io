#!/usr/bin/env python3
import os
import sys
from os import path
import tempfile
from datetime import datetime, timezone, timedelta
from subprocess import run
import shutil

if len(sys.argv) <= 1:
    print("Error: Need path to file being updated.")
    sys.exit(1)
stem, ext = path.splitext(path.basename(sys.argv[1]))
ext = ext.removeprefix(".")
is_yaml = ext == "yaml" or ext == "yml"
is_markdown = ext == "md"
is_config = stem == "_config" and is_yaml
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
found_frontmatter = is_config
found_date = False
date_key = "last_updated" if is_config else "data"
with open(notes_path, "rt") as f:
    f.seek(0, os.SEEK_END)
    len = f.tell()
    f.seek(0, os.SEEK_SET)
    is_frontmatter = is_config
    before_frontmatter = not is_config
    while f.tell() < len:
        line = f.readline()
        if before_frontmatter:
            pre += line
            if line.strip() == "---":
                before_frontmatter = False
                is_frontmatter = True
                found_frontmatter = True
        elif is_frontmatter:
            is_date = line.strip().startswith("%s:" % date_key)
            if not is_config and line.strip() == "---":
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
if not found_frontmatter and not is_config:
    post = "---\n" + pre
    pre = "---\n"
with tempfile.NamedTemporaryFile(suffix=".%s" % ext, mode="wt", delete_on_close=False, delete=False) as f:
    fpath = f.name
    f.write(pre)
    f.write("%s: %s\n" % (date_key, fmt))
    f.write(post)

shutil.copyfile(fpath, notes_path)
os.remove(fpath)
