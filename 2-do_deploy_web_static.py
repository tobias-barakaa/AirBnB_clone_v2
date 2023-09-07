#!/usr/bin/python3
from fabric import api as fab


def do_deploy(archive_path):
    """Deploys the given archive to the web servers."""

    # Check if the archive exists
    if not fab.exists(archive_path):
        return False

    # Upload the archive to the web servers
    fab.put(archive_path, "/tmp")

    # Uncompress the archive to the /data/web_static/releases/<archive filename without extension> directory on the web server
    fab.run("mkdir -p /data/web_static/releases/{}".format(
        archive_path.split(".tgz")[0]))
    fab.run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(
        archive_path, archive_path.split(".tgz")[0]))

    # Delete the archive from the web server
    fab.run("rm /tmp/{}".format(archive_path))

    # Delete the symbolic link /data/web_static/current from the web server
    fab.run("rm -rf /data/web_static/current")

    # Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
    fab.run("ln -s /data/web_static/releases/{} /data/web_static/current".format(
        archive_path.split(".tgz")[0]))

    return True


if __name__ == "__main__":
    archive_path = "/path/to/archive.tgz"

    # Deploy the archive
    if do_deploy(archive_path):
        print("New version deployed!")
    else:
        print("Failed to deploy the archive.")
