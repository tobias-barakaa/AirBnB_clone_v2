#!/usr/bin/python3
"""Fabric script to generate a .tgz archive from web_static folder"""

from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from web_static folder."""
    try:
        # Create the "versions" directory if it doesn't exist
        local("mkdir -p versions")

        # Create a filename with the current date and time
        now = datetime.now()
        formatted_date = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(formatted_date)

        # Compress the web_static folder into a .tgz archive
        local("tar -cvzf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None
