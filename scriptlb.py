#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import os
from subprocess import call

os.system("nohup sudo xr -dr --verbose --server tcp:0:80 --backend 10.1.3.11:3000 --backend 10.1.3.12:3000 --backend 10.1.3.13:3000 &")