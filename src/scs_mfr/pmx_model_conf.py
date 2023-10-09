#!/usr/bin/env python3

"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The pmx_model_conf utility is used to specify how Greengrass data interpretation models are to be accessed:

* UDS_PATH - the Unix domain socket for communication between the particulates sampler and the inference server
* INTERFACE - the format of the request
* SPECIES: RESOURCE_NAME - the model resource for each particle size

The particulates_sampler and Greengrass container must be restarted for changes to take effect.

SYNOPSIS
pmx_model_conf.py [{ [-u UDS_PATH] [-i INTERFACE] | -d }] [-v]

EXAMPLES
./pmx_model_conf.py -u pipes/lambda-pmx-model.uds -i s2 -v

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-pmx-model.uds", "model-interface": "s2"}

FILES
~/SCS/conf/pmx_model_conf.json

SEE ALSO
scs_dev/particulates_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_core.model.pmx.pmx_model_conf import PMxModelConf

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_model_conf import CmdModelConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdModelConf(PMxModelConf.interfaces())

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('pmx_model_conf', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # PMxModelConf...
    conf = PMxModelConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = PMxModelConf.load(Host, skeleton=True)

        if conf is None and not cmd.is_complete():
            logger.error("No configuration is stored - you must therefore set all fields.")
            cmd.print_help(sys.stderr)
            exit(2)

        uds_path = cmd.uds_path if cmd.uds_path else conf.uds_path
        model_interface = cmd.model_interface if cmd.model_interface else conf.model_interface

        if uds_path is None:
            logger.error("the UDS path must be set.")
            exit(2)

        if model_interface is None:
            logger.error("the interface code must be set.")
            exit(2)

        conf = PMxModelConf(uds_path, model_interface)
        conf.save(Host)

    if cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
