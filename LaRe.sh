#!/bin/bash
#check La Regencia house every 30 seconds
while true; do python3.7 websitechanges.py --folder ./LRegencia/ --url https://www.on-site.com/apply/property/1360 --to cjunwei724@163.com --smtpemail newhouseavailable@163.com --smtppass WXCJKVYMVHXDGAKX --threshold 0.95; sleep 30; done
