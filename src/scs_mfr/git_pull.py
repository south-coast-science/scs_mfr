#!/usr/bin/env python3

"""
Created on 24 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The git_pull utility is used to perform a git pull on all the repos in the ~/SCS directory. When the pulls
are complete, a JSON document is saved, summarising the state of the installed repos. When run without the --pull flag
the git_pull utility  reports on the most recent operation.

Note that the utility skips private repos (such as scs_exegesis).

Warning: the overall operation is not atomic - if one or more repo pulls fail, the resulting set will lose consistency.
The "success" field  report indicates whether the outcome is consistent.

SYNOPSIS
git_pull.py [-p [-t TIMEOUT]] [-v]

EXAMPLES
./git_pull.py -vp

DOCUMENT EXAMPLE
{"pulled-on": "2021-02-27T08:37:09Z", "success": true,
"installed": ["scs_core", "scs_dev", "scs_dfe_eng", "scs_host_cpc", "scs_mfr", "scs_psu"],
"pulled": ["scs_core", "scs_dev", "scs_dfe_eng", "scs_host_cpc", "scs_mfr", "scs_psu"],
"excluded": []}

FILES
~/SCS/conf/git_pull.json
"""

import os
import sys

from scs_core.data.datetime import LocalizedDatetime
from scs_core.data.json import JSONify

from scs_core.estate.git_pull import GitPull

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_git_pull import CmdGitPull


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    pulled = []
    excluded = []
    success = True

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdGitPull()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('git_pull', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    start = LocalizedDatetime.now()

    root = Host.scs_path()
    installed = GitPull.dirs(root)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        if cmd.pull:
            for repo in installed:
                if GitPull.excludes(repo):
                    logger.info("%s: excluded - skipping" % repo)
                    excluded.append(repo)
                    continue

                path = os.path.join(root, repo)

                if not GitPull.is_clone(path):
                    logger.error("%s: not a git clone - skipping" % repo)
                    success = False
                    continue

                try:
                    logger.info(repo)
                    repo_success, stdout, stderr = GitPull.pull_repo(path, cmd.timeout)

                    if cmd.verbose:
                        print(stdout, end='', file=sys.stderr)
                        print(stderr, end='', file=sys.stderr)

                    if not repo_success:
                        logger.error("%s: pull failed" % repo)
                        success = False
                        continue

                except TimeoutError:
                    logger.error("%s: timed out" % repo)
                    success = False
                    continue

                pulled.append(repo)

            git = GitPull(start, success, installed, pulled, excluded)
            git.save(Host)

        else:
            git = GitPull.load(Host)


        # ----------------------------------------------------------------------------------------------------------------
        # end...

        print(JSONify.dumps(git))

    except KeyboardInterrupt:
        print(file=sys.stderr)

    finally:
        exit(0 if success else 1)
