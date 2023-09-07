#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

import os.path
from fabric.api import env, put, run

env.hosts = ["100.25.196.36", "52.87.215.223"]

def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False

    # Extract filename and name without extension
    filename = os.path.basename(archive_path)
    name = os.path.splitext(filename)[0]

    # Upload the archive to the /tmp/ directory on the server
    if put(archive_path, "/tmp/{}".format(filename)).failed:
        return False

    # Create the release directory
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed:
        return False

    # Uncompress the archive into the release directory
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(filename, name)).failed:
        return False

    # Remove the uploaded archive
    if run("rm /tmp/{}".format(filename)).failed:
        return False

    # Move files from the uncompressed folder to the release folder
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed:
        return False

    # Remove the empty web_static directory
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed:
        return False

    # Delete the existing symbolic link
    if run("rm -rf /data/web_static/current").failed:
        return False

    # Create a new symbolic link
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed:
        return False

    return True
