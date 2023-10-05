#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web servers,
using the function deploy:
"""

from fabric.api import local, env, run, put
import datetime
from pathlib import Path


env.hosts = ['18.206.206.50', '35.175.104.89']


def do_pack():
    """
    Function to pack all contents of the web static
    folder into a tgz archive
    """

    if local('mkdir -p versions').failed:
        return None

    curr_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    arch_path = 'versions/web_static_{}.tgz'.format(curr_time_str)
    if local('cd ./web_static && tar -czvf ../{} *'.format(arch_path)).failed:
        return None
    else:
        return(arch_path)


def do_deploy(archive_path):
    """
    Function to Upload the archive to the /tmp/ directory of the web server

    Create a new the symbolic link /data/web_static/current on
    the web server linked to the new version of your code
    (/data/web_static/releases/<archive filename without extension>)

    Args:
        archive_path(str): Archive to be deployed

    Returns:
        (bool): True if successful else False
    """

    p = Path(archive_path)

    if not p.exists():
        return False

    arch_folder = '/data/web_static/releases'
    if put(archive_path, '/tmp/').failed:
        return False
    if (run('tar -xzf /tmp/{} -C {} --one-top-level'.
            format(p.name, arch_folder)).failed):
        return False
    if run('rm -rf /tmp/{}'.format(p.name)).failed:
        return False

    sym_link = "/data/web_static/current"
    if (run('ln -sf -T {}/{} {}'.
            format(arch_folder, p.stem, sym_link)).failed):
        return False

    return True


created_archive = None


def deploy():
    """
    Call the do_pack() function and store the path of the created archive
    Call the do_deploy(archive_path) function,
    using the new path of the new archive
    Return the return value of do_deploy

    Returns:
        (bool): Return value of `do_deploy`
    """
    global created_archive
    created_archive = do_pack() if not created_archive else created_archive
    if not created_archive:
        return False

    return do_deploy(created_archive)
