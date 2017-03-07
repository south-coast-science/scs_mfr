#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

workflow:
  1: ./scs_mfr/device_id.py
> 2: ./scs_mfr/osio_api_auth.py
  3: ./scs_mfr/osio_device_create.py
  4: ./scs_mfr/osio_publication.py

Creates APIAuth document.

command line example:
./scs_mfr/osio_api_auth.py -v -s south-coast-science-dev 43308b72-ad41-4555-b075-b4245c1971db
"""

import sys

from scs_core.data.json import JSONify
from scs_core.osio.client.api_auth import APIAuth

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_api_auth import CmdOSIOAPIAuth


# TODO: check whether the ORG_ID exists on OSIO?

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOAPIAuth()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        auth = APIAuth(cmd.org_id, cmd.api_key)
        auth.save(Host)

    else:
        auth = APIAuth.load_from_host(Host)

    print(JSONify.dumps(auth))
