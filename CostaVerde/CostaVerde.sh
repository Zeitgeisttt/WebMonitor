#!/bin/bash
#check CVV house every 30 seconds
while true; do python ../webmonitor.py --folder ./ --url https://www.on-site.com/apply/property/1166 --to example@xxx.com --smtpemail newhouseavailable@163.com --smtppass WXCJKVYMVHXDGAKX --threshold 0.95; sleep 30; done
