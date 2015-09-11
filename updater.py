import requests
import re
import base64
import os
from datetime import datetime
from sh import git

ips = []
__folder__ = os.path.split(__file__)[0]
regex = re.compile(r"\/(.+)\/")
l = requests.get("https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf").text

for i in l.split("\n")[1:]:
    if i and regex.search(i):
        ips.append(regex.search(i).group())


with open(os.path.join(__folder__, "rawlist.txt"), "w") as fp:
    for i in ips:
        fp.write(i+"\n")

with open(os.path.join(__folder__, "list.txt"), 'w') as fp:
    for i in ips:
        fp.write("|{}\n".format(i))

if git.status("--short") != "":
    git.add(".")
    git.commit("-m", "update")
    git.push()
