#!/usr/bin/env python3

"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The pmx_model_conf utility is used to specify how Greengrass data interpretation models are to be accessed:

* UDS_PATH - the Unix domain socket for communication between the particulates sampler and the inference server
* INTERFACE - the format of the request and response
* MODEL - Greengrass ML configuration template

The particulates_sampler and Greengrass container must be restarted for changes to take effect.

SYNOPSIS
pmx_model_conf.py [{ -l | [-u UDS_PATH] [-i INTERFACE] [-m MAP] | -d }] [-v]

EXAMPLES
./pmx_model_conf.py -u pipes/lambda-pmx-model.uds -i s2 -m oM.2 -v

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-pmx-model.uds", "model-interface": "s2", "model-map": "oM.2"}

FILES
~/SCS/conf/pmx_model_conf.json

SEE ALSO
scs_dev/particulates_sampler
scs_mfr/aws_group_setup
"""

import sys

from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration
from scs_core.data.json import JSONify

from scs_core.model.model_conf import ModelConf
from scs_core.model.model_mapping import ModelMapping
from scs_core.model.gas.gas_model_conf import GasModelConf
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

    group_configuration = AWSGroupConfiguration.load(Host)
    ml = None if group_configuration is None else group_configuration.ml

    gas_model_conf = GasModelConf.load(Host)
    pmx_model_conf = PMxModelConf.load(Host)

    # ----------------------------------------------------------------------------------------------------------------
    # validation...

    try:
        gg_ml_template = ModelConf.gg_ml_template(gas_model_conf, pmx_model_conf)
    except ValueError as ex:
        gg_ml_template = None

    if cmd.model_map is not None and gg_ml_template is not None and ml is not None:
        if gg_ml_template != ml:
            logger.error("WARNING: the specified map '%s' does not match the server template '%s'" %
                         (cmd.model_map, ml))


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = PMxModelConf.load(Host, skeleton=True)

        if conf is None and not cmd.is_complete():
            logger.error("No configuration is stored - you must therefore set all fields.")
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.model_interface is not None and cmd.model_interface not in PMxModelConf.interfaces():
            logger.error("interface '%s' cannot be found." % cmd.model_interface)
            exit(2)

        if cmd.model_map is not None and cmd.model_map not in ModelMapping.names():
            logger.error("model map '%s' cannot be found." % cmd.model_map)
            exit(2)

        uds_path = cmd.uds_path if cmd.uds_path else conf.uds_path
        model_interface = cmd.model_interface if cmd.model_interface else conf.model_interface
        model_map = ModelMapping.map(cmd.model_map) if cmd.model_map else conf.model_map

        if uds_path is None:
            logger.error("the UDS path must be set.")
            exit(2)

        if model_interface is None:
            logger.error("the interface code must be set.")
            exit(2)

        if model_map is None:
            logger.error("the model map must be set.")
            exit(2)

        conf = PMxModelConf(uds_path, model_interface, model_map)
        conf.save(Host)

    if cmd.delete and pmx_model_conf is not None:
        pmx_model_conf.delete(Host)
        pmx_model_conf = None

    if pmx_model_conf:
        print(JSONify.dumps(pmx_model_conf))
