#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using the function do_deploy:
"""

from fabric.api import env, run, put
import datetime
from pathlib import Path


env.hosts = ['18.206.206.50', '35.175.104.89']


def do_deploy(archive_path):
    """
    Function to Upload the archive to the /tmp/ directory of the web server

    Create a new the symbolic link /data/web_static/current on the web server,
    linked to the new version of your code
    (/data/web_static/releases/<archive filename without extension>)

    Args:
        archive_path(str): Archive to be deployed

    Returns:
        (bool): True if successful else False
    """

    p = Path(archive_path)

    if not p.exists():
        return False

    arch_folder = '/data/web_static/releases/'
    if put(archive_path, '/tmp/').failed:
        return False
    if (run('tar -xzf /tmp/{} -C {} --one-top-level'.
            format(p.name, arch_folder)).failed):
        return False
    if run('rm -rf /tmp/{}'.format(p.name)).failed:
        return False

    sym_link = "/data/web_static/current"
    if run('ln -sf -T {}/{} {}'.format(arch_folder, p.stem, sym_link)).failed:
        return False

    return True
