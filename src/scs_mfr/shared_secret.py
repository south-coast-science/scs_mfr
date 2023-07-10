#!/usr/bin/env python3

"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The shared_secret utility generates a digest key / password used by the CognitoDevices security subsystem.

When the shared secret is generated, the utility attempts to update its CognitoDevices record. When a shared
secret is generated for the first time on a new device, this update should be inhibited using the
--ignore-credentials flag.

SYNOPSIS
shared_secret.py [{ -g [-i] | -d }] [-v]

EXAMPLES
./shared_secret.py -g

DOCUMENT EXAMPLE
{"key": "########"}

FILES
~/SCS/conf/shared_secret.conf

SEE ALSO
scs_dev/control_receiver
"""

import requests
import sys

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_device_finder import CognitoDeviceIntrospector
from scs_core.aws.security.cognito_device_manager import CognitoDeviceManager
from scs_core.aws.security.cognito_login_manager import CognitoLoginManager

from scs_core.data.json import JSONify

from scs_core.sys.logging import Logging
from scs_core.sys.shared_secret import SharedSecret

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_shared_secret import CmdSharedSecret


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    auth = None

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSharedSecret()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('shared_secret', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SHTConf...
    secret = SharedSecret.load(Host)

    # CognitoDeviceCredentials...
    gatekeeper = CognitoLoginManager(requests)
    finder = CognitoDeviceIntrospector(requests)

    # CognitoDeviceManager...
    manager = CognitoDeviceManager(requests)


    # ------------------------------------------------------------------------------------------------------------
    # authentication...

    if not cmd.ignore_credentials:
        credentials = CognitoDeviceCredentials.load_credentials_for_device(Host, strict=False)

        if credentials:
            auth = gatekeeper.device_login(credentials)

            if not auth.is_ok():
                logger.error("existing credentials are invalid, so the Cognito record cannot be updated.")
                exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.generate:
        secret = SharedSecret(SharedSecret.generate())
        secret.save(Host)

        if not cmd.ignore_credentials:
            new_credentials = CognitoDeviceCredentials.load_credentials_for_device(Host)
            manager.update_self(auth.id_token, new_credentials)

    if cmd.delete and secret is not None:
        secret.delete(Host)
        secret = None

    if secret:
        print(JSONify.dumps(secret))
