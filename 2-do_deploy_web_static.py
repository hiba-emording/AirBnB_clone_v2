#!/usr/bin/python3
# a Fabric script that distributes an archive to web server.

from fabric.api import put, run, env
from os.path import exists


env.hosts = ['18.204.7.236', '52.91.128.49']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers
    """

    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        archive_name_without_extension = file_name.split(".")[0]

        deployment_path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')

        run('mkdir -p {}{}/'
            .format(deployment_path, archive_name_without_extension))

        run('tar -xzf /tmp/{} -C {}{}/'
            .format(file_name, deployment_path, archive_name_without_extension)
            )

        run('rm /tmp/{}'.format(file_name))

        run('mv {0}{1}/web_static/* {0}{1}/'
            .format(deployment_path, archive_name_without_extension))

        run('rm -rf {}{}/web_static'
            .format(deployment_path, archive_name_without_extension))

        run('rm -rf /data/web_static/current')

        run('ln -s {}{}/ /data/web_static/current'
            .format(deployment_path, archive_name_without_extension))

        return True

    except Exception as e:
        return False
