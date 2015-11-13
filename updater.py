#!/bin/env python3
import requests
import re
import base64
import os
from datetime import datetime
from sh import git

ips = []
__folder__ = os.path.split(__file__)[0]
if __folder__:
    os.chdir(__folder__)
regex = re.compile(r"\/(.+)\/")
l = requests.get("https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf").text

print("load changes")
git.pull("--all")
git.reset("origin/master", "--hard")
git.pull()

print("Finish download")
for i in l.split("\n")[1:]:
    if i and regex.search(i):
        ips.append(regex.search(i).groups()[0])


with open(os.path.join(__folder__, "rawlist.txt"), "w") as fp:
    for i in ips:
        fp.write(i+"\n")

with open(os.path.join(__folder__, "list.txt"), 'w') as fp:
    # s = "[AutoProxy 0.2.9]\n"
    for i in ips:
        fp.write("||{}\n".format(i))
    # s = base64.b64encode(s.encode('utf8')).decode()
    # for i in range(0, len(s), 64):
        # fp.write(s[i:i+64])
        # fp.write("\n")

if git.status("--short") != "":
    print("updating")
    git.add(".")
    git.commit("-m", "update")
    git.push()
    print("updating finished")
