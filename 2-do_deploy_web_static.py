#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it.

    Args:
        archive_path (str): The path to the archive to be deployed.

    Returns:
        True if all operations have been done correctly, otherwise False.
    """
    if not exists(archive_path):
        return False

    try:
        # Get the filename without the extension
        filename = archive_path.split('/')[-1].split('.')[0]

        # Upload the archive to /tmp/ directory on the remote server
        put(archive_path, "/tmp/")

        # Create the target directory for the release
        run("mkdir -p /data/web_static/releases/{}/".format(filename))

        # Extract the archive to the target directory
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(filename, filename))

        # Remove the uploaded archive from the server
        run("rm /tmp/{}.tgz".format(filename))

        # Move the contents to the appropriate directory
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(filename, filename))

        # Remove the empty web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename))

        # Update the symbolic link
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(filename))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
