#!/usr/bin/python3
"""Fabric script to distribute an archive to web servers"""

from fabric.api import env, put, run, local
import os

env.user = 'ubuntu'
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """Distributes an archive to web servers and deploys it"""
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, "/tmp/")

        # Extract filename without extension from archive_path
        filename = os.path.basename(archive_path)
        filename_noext = os.path.splitext(filename)[0]

        # Create the release directory
        run("mkdir -p /data/web_static/releases/{}".format(filename_noext))

        # Uncompress the archive into the release directory
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(filename, filename_noext))

        # Delete the archive from /tmp/
        run("rm /tmp/{}".format(filename))

        # Move files from the uncompressed folder to the release folder
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(filename_noext, filename_noext))

        # Remove the empty web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static".format(filename_noext))

        # Delete the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(filename_noext))

        print("New version deployed!")

        return True
    except Exception as e:
        return False
