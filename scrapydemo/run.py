#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

task = None
try:
    task = sys.argv[1]
except:
    pass
if task:
    os.system("scrapy crawl {}".format(task))
else :
    os.system("scrapy crawl yousuu")