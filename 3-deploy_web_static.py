#!/usr/bin/python3
"""Fabric script to create and distribute an archive to web servers"""

from fabric.api import run, env, put
from os.path import exists


env.hosts = ['18.204.7.236', '52.91.128.49']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Create a compressed archive of the web_static folder."""
    from fabric.api import local
    from datetime import datetime

    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        archive_file = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_file))
        return archive_file
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to web servers."""
    if not exists(archive_path):
        return False

    try:
        file = archive_path.split("/")[-1]
        name = file.split(".")[0]

        if put(archive_path, "/tmp/{}".format(file)).failed:
            return False
        if run("rm -rf /data/web_static/releases/{}/"
               .format(name)).failed:
            return False
        if run("mkdir -p /data/web_static/releases/{}/"
               .format(name)).failed:
            return False
        if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
               .format(file, name)).failed:
            return False
        if run("rm /tmp/{}".format(file)).failed:
            return False
        if run("mv /data/web_static/releases/{}/web_static/* "
               "/data/web_static/releases/{}/"
               .format(name, name)).failed:
            return False
        if run("rm -rf /data/web_static/releases/{}/web_static"
               .format(name)).failed:
            return False
        if run("rm -rf /data/web_static/current").failed:
            return False
        if run("ln -s /data/web_static/releases/{}/ "
               "/data/web_static/current"
               .format(name)).failed:
            return False
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive to web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
