#!/usr/bin/env bash
pyarmor pack -e " -F --icon=udef/my-app.ico --noconsole --add-data /home/sr9000/.local/lib/python3.6/site-packages/qtmodern/resources/*:qtmodern/resources --add-data udef/my-app.ico:./udef --hidden-import=pkg_resources.py2_warn" main.py
