#!/usr/bin/python3
"""
Fabric script (based on the file 3-deploy_web_static.py) that
deletes out-of-date archives, using the function do_clean:
"""

from fabric.api import local, env, run, put, runs_once
import datetime
from pathlib import Path


env.hosts = ['18.206.206.50', '35.175.104.89']


l_clean = False


def do_clean(number=0):
    """
    Function to delete out of date archives

    Args:
        number(int): Number of the archives, including the most recent, to kp.

                     If number is 0 or 1, keep only the most recent
                     version of your archive.
                     If number is 2, keep the most recent, and second
                     most recent versions of your archive.
    """

    global l_clean
    vs = './versions'
    rses = '/data/web_static/releases'
    number = 1 if int(number) == 0 else int(number)

    if not l_clean:
        local('rm -f $(ls -1rt {}/*.tgz | head -n -{})'.format(vs, number))
        l_clean = True
    run('rm -rf $(ls -1drt {}/web_static* | head -n -{})'.format(rses, number))
