#!/usr/bin/env python3

"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The gas_model_conf utility is used to specify how Greengrass data interpretation models are to be accessed:

* UDS_PATH - the Unix domain socket for communication between the gas sampler and the inference server
* INTERFACE - the format of the request and response
* MODEL - Greengrass ML configuration template

If present, the gas model (set by gas_model_conf utility) must match the PMx model.

The gases_sampler and Greengrass container must be restarted for changes to take effect.

SYNOPSIS
gas_model_conf.py [{ -l | [-u UDS_PATH] [-i INTERFACE] [-m MAP] | -d }] [-v]

EXAMPLES
./gas_model_conf.py -u pipes/lambda-gas-model.uds -i vE -m oM.2

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-gas-model.uds", "model-interface": "vE", "model-map": "oM.2"}

FILES
~/SCS/conf/gas_model_conf.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/aws_group_setup
"""

import sys

from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration

from scs_core.data.json import JSONify

from scs_core.model.model_map import ModelMap
from scs_core.model.gas.gas_model_conf import GasModelConf
from scs_core.model.pmx.pmx_model_conf import PMxModelConf

from scs_core.sys.logging import Logging

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_model_conf import CmdModelConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdModelConf(GasModelConf.interfaces())

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    # logging...
    Logging.config('gas_model_conf', verbose=cmd.verbose)
    logger = Logging.getLogger()

    logger.info(cmd)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    group_configuration = AWSGroupConfiguration.load(Host)

    gas_model_conf = GasModelConf.load(Host)
    pmx_model_conf = PMxModelConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        gas_model_conf = GasModelConf.load(Host, skeleton=True)

        if gas_model_conf is None and not cmd.is_complete():
            logger.error("No configuration is stored - you must therefore set the UDS path and the interface.")
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.model_interface is not None and cmd.model_interface not in GasModelConf.interfaces():
            logger.error("interface '%s' cannot be found." % cmd.model_interface)
            exit(2)

        if cmd.model_map is not None and cmd.model_map not in ModelMap.names():
            logger.error("model map '%s' cannot be found." % cmd.model_map)
            exit(2)

        uds_path = cmd.uds_path if cmd.uds_path else gas_model_conf.uds_path
        model_interface = cmd.model_interface if cmd.model_interface else gas_model_conf.model_interface
        model_map = ModelMap.map(cmd.model_map) if cmd.model_map else gas_model_conf.model_map

        if uds_path is None:
            logger.error("the UDS path must be set.")
            exit(2)

        if model_interface is None:
            logger.error("the interface code must be set.")
            exit(2)

        if model_map is None:
            logger.error("the model map must be set.")
            exit(2)

        gas_model_conf = GasModelConf(uds_path, model_interface, model_map)
        gas_model_conf.save(Host)

    elif cmd.delete and gas_model_conf is not None:
        gas_model_conf.delete(Host)
        gas_model_conf = None

    if gas_model_conf:
        if group_configuration:
            try:
                if group_configuration.configuration_is_mismatched(gas_model_conf, pmx_model_conf):
                    logger.error("WARNING: the specified map '%s' does not match the server template" %
                                 gas_model_conf.model_map_name)
            except ValueError:
                logger.error("WARNING: the specified map '%s' is different to the pmx map '%s'" %
                             (gas_model_conf.model_map_name, pmx_model_conf.model_map_name))

        print(JSONify.dumps(gas_model_conf))
