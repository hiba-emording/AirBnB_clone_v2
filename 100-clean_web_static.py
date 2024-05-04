#!/usr/bin/python3
"""Fabric script to delete out-of-date archives."""

from fabric.api import *
import os


env.hosts = ['18.204.7.236', '52.91.128.49']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_clean(number=0):
    """Delete out-of-date archives."""
    number = int(number)
    if number < 1:
        number = 1

    with lcd("versions"):
        archives = local("ls -t", capture=True).split()
        for archive in archives[number:]:
            local("rm -f {}".format(archive))

    with cd("/data/web_static/releases"):
        releases = run("ls -t").split()
        for release in releases[number:]:
            run("rm -rf {}".format(release))
