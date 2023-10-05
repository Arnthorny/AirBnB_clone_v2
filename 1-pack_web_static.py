#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB
Clone repo, using the function `do_pack`
"""

from fabric.api import local
import datetime


def do_pack():
    """
    Function to pack all contents of the web static
    folder into a tgz archive

    Returns:
        (str): Path to created archive
    """

    if local('mkdir -p versions').failed:
        return None

    curr_time_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    arch_path = 'versions/web_static_{}.tgz'.format(curr_time_str)
    if local('cd ./web_static && tar -czvf ../{} *'.format(arch_path)).failed:
        return None
    else:
        return(arch_path)
