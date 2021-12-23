#!/bin/bash
#check La Regencia house every 30 seconds
while true; do python ../webmonitor.py --folder ./ --url https://www.on-site.com/apply/property/1360 --to example@xxx.com --smtpemail newhouseavailable@163.com --smtppass WXCJKVYMVHXDGAKX --threshold 0.95; sleep 30; done
