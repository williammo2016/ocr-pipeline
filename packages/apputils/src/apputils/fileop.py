"""Useful file operations
"""
from zipfile import ZipFile
from os import walk, remove, makedirs
from os.path import join, splitext, exists
from shutil import rmtree
from hashlib import sha256

module_conf = {
    "zip_ext": ".zip"
}


def zip_directory(directory):
    """Zip a directory

    Paramters
        directory (:func:`str`): Directory to zip

    Returns:
        (:func:`str`): Name of the archive
    """
    archive_name = directory + module_conf["zip_ext"]
    zip_dir = ZipFile(archive_name, "w")

    for root, folders, files in walk(directory):
        for item in folders+files:
            orig_path = join(root, item)
            dest_path = orig_path[len(directory):]

            zip_dir.write(orig_path, dest_path)

    rmtree(directory)  # Clean directory
    return archive_name


def unzip_directory(archive):
    """Unzip an archive

    Paramters
        archive (:func:`str`): Archive to unzip

    Returns:
        (:func:`str`): Name of the directory
    """
    zip_dir = ZipFile(archive, "r")
    directory = splitext(archive)[0]

    zip_dir.extractall(directory)
    remove(archive)

    return directory


def create_directories(dir_conf, prefix=None):
    """Create application directories and subdirectories given a configuration dictionary

    Parameters
        dir_conf (:func:`str`): List of directories to create
        prefix (:func:`str` or None): Root directory for the current tree

    Raises:
        ValueError: If there is a subdirectory with no root or if the subdirectory key is not a dictionary
    """
    dirnames = [d for d in dir_conf.values() if isinstance(d, str)]

    for dirname in dirnames:
        dirpath = join(prefix, dirname) if prefix is not None else dirname

        if not exists(dirpath):
            makedirs(dirpath)

    dir_keys = dir_conf.keys()
    roots = [d for d in dir_keys if d.endswith("_root") and d.split("_root")[0] in dir_keys]
    dir_dicts = [d for d in dir_conf.values() if not isinstance(d, str)]

    # More dictionaries than roots
    if len(roots) < len(dir_dicts):
        raise TypeError("All subdirectory must have a _root key")

    for r in roots:
        key = r.split("_root")[0]
        subfolders = dir_conf[key]

        if not isinstance(subfolders, dict):
            raise TypeError("Expecting dict, got "+str(type(subfolders)))

        if prefix is not None:
            prefix = join(prefix, dir_conf[r])
        else:
            prefix = dir_conf[r]

        create_directories(subfolders, prefix)


def file_checksum(filename):
    """Return the sha256 digest of a file

    Parameters:
        filename (:func:`str`): The file to hash

    Returns:
        (:func:`str`): Hash of the file
    """
    return sha256(open(filename).read()).hexdigest()
