#!/usr/bin/env python3

"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The shared_secret utility generates a digest key used by the scs_analysis/mqtt_control and scs_dev/control_receiver
utilities. The key is typically generated when a device is manufactured, and securely stored on a remote device
management system.

SYNOPSIS
shared_secret.py [{ -g | -d }] [-v]

EXAMPLES
./shared_secret.py -g

DOCUMENT EXAMPLE
{"key": "sxBhncFybpbMwZUa"}

FILES
~/SCS/conf/shared_secret.conf

SEE ALSO
scs_dev/control_receiver
"""

import requests
import sys

from scs_core.aws.security.cognito_device import CognitoDeviceCredentials
from scs_core.aws.security.cognito_device_finder import CognitoDeviceIntrospector
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


    # ------------------------------------------------------------------------------------------------------------
    # authentication...

    credentials = CognitoDeviceCredentials.load_credentials_for_device(Host, strict=False)

    if credentials:
        auth = gatekeeper.device_login(credentials)

        if auth.is_ok():
            finder = CognitoDeviceIntrospector(requests)
            device = finder.find_self(auth.id_token)
            logger.info(device)

        else:
            logger.error("WARNING: existing credentials are invalid, so the Cognito record cannot be updated.")


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.generate:
        secret = SharedSecret(SharedSecret.generate())
        secret.save(Host)

        # TODO: update cognito identity

    if cmd.delete and secret is not None:
        secret.delete(Host)
        secret = None

    if secret:
        print(JSONify.dumps(secret))
