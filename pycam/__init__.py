# -*- coding: utf-8 -*-
"""
Copyright 2008 Lode Leroy

This file is part of PyCAM.

PyCAM is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyCAM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyCAM.  If not, see <http://www.gnu.org/licenses/>.
"""


import os
import subprocess


try:
    from Version import VERSION

except ImportError:
    # Failed to import Version.py, we must be running out of a git
    # checkout, so generate the version info from git tags.

    #
    # These variables should only be changed by the release manager when
    # creating a new stable release branch.
    #
    # In master:
    #     * 'parent_branch' stays set to 'master'
    #     * 'tag_glob' is changed to the glob for the next set of releases.
    #
    # In the new stable branch:
    #     * 'parent_branch' is set to the name of the new stable branch.
    #     * 'tag_glob' stays set to the glob for release tags on this branch.
    #
    parent_branch = "master"
    tag_glob = "v0.*"

    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    try:
        current_branch = subprocess.check_output(['git', 'rev-parse',
                                                  '--abbrev-ref',
                                                  'HEAD'],
                                                 cwd=repo_dir)
        current_branch = current_branch.strip()

        git_describe = subprocess.check_output(["git", "describe",
                                                "--always", "--dirty",
                                                "--tags", "--match",
                                                tag_glob], cwd=repo_dir)
        # remove the "v" prefix
        git_describe = git_describe.strip().lstrip("v")

        if current_branch == parent_branch:
            # We're on master or on a stable/release branch, so the
            # version number is just the 'git describe' output.
            VERSION = git_describe

        else:
            # We're on a temporary branch, so make a version number that
            # sorts as *older than* nearby release versions.
            parts = git_describe.split('-')
            parts[0] = parts[0] + '~' + current_branch
            VERSION = '-'.join(parts)

        # No matter how we made the version string, replace every "-"
        # with ".", because that's what Debian version numbers expect.
        # https://www.debian.org/doc/debian-policy/ch-controlfields.html#s-f-Version
        VERSION = VERSION.replace('-', '.')

    except subprocess.CalledProcessError:
        # No pycam/Version.py and git failed to give us a version number, give up.
        VERSION = "0.0-unknown"


FILTER_CONFIG = (("Config files", "*.conf"),)
DOC_BASE_URL = "http://pycam.sourceforge.net/%s/"


class GenericError(Exception):
    pass


class InvalidValueError(GenericError):
    pass


class CommunicationError(GenericError):
    pass
