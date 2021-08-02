#!/bin/bash
#check Crossroad house every 30 seconds
while true; do python3.7 websitechanges.py --folder ./LJCross/ --url https://www.on-site.com/apply/property/21385 --to cjunwei724@163.com --smtpemail newhouseavailable@163.com --smtppass WXCJKVYMVHXDGAKX --threshold 0.95; sleep 30; done
