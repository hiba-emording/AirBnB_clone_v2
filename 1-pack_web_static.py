#!/usr/bin/python3
# a Fabric script that generates a.tgz archive from contents of web_static

from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from contents of web_static folder
    """
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    archive_name = "versions/web_static_{}.tgz".format(timestamp)

    local("mkdir -p versions")

    result = local("tar -cvzf {} web_static".format(archive_name))

    if result.succeeded:
        return archive_name
    else:
        return None
