#!/usr/bin/env python3

"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The gas_model_conf utility is used to specify how Greengrass data interpretation models are to be accessed:

* UDS_PATH - the Unix domain socket for communication between the gas sampler and the inference server
* INTERFACE - the format of the request
* GROUP - the performance parameters of the model(s) to be used (not required for VB or vB2)

Note that the template name for the AWS group is specified by the group name as set here.

The gases_sampler and Greengrass container must be restarted for changes to take effect.

SYNOPSIS
gas_model_conf.py [{ -l | [-u UDS_PATH] [-i INTERFACE] [-g GROUP] | -d }] [-v]

EXAMPLES
./gas_model_conf.py -u pipes/lambda-gas-model.uds -i vE -g oE.1

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-gas-model.uds", "model-interface": "vE", "model-compendium-group": "oE.1"}

FILES
~/SCS/conf/gas_model_conf.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/aws_group_setup
"""

import sys

from scs_core.aws.greengrass.aws_group_configuration import AWSGroupConfiguration

from scs_core.data.json import JSONify

from scs_core.model.catalogue.model_compendium_group import ModelCompendiumGroup
from scs_core.model.gas.gas_model_conf import GasModelConf

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
    # validation...

    group_configuration = AWSGroupConfiguration.load(Host)
    ml = None if group_configuration is None else group_configuration.ml

    if cmd.model_compendium_group is not None and ml is not None:
        if cmd.model_compendium_group != ml:
            logger.error("WARNING: the specified group '%s' does not match the server template '%s'" %
                         (cmd.model_compendium_group, ml))


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # GasModelConf...
    conf = GasModelConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.list:
        print(JSONify.dumps(ModelCompendiumGroup.list()))

    elif cmd.set():
        conf = GasModelConf.load(Host, skeleton=True)

        if conf is None and not cmd.is_complete():
            logger.error("No configuration is stored - you must therefore set the UDS path and the interface.")
            cmd.print_help(sys.stderr)
            exit(2)

        if cmd.model_compendium_group is not None and \
                cmd.model_compendium_group not in ModelCompendiumGroup.list():
            logger.error("group '%s' cannot be found." % cmd.model_compendium_group)
            exit(2)

        uds_path = cmd.uds_path if cmd.uds_path else conf.uds_path
        model_interface = cmd.model_interface if cmd.model_interface else conf.model_interface
        model_compendium_group = cmd.model_compendium_group if cmd.model_compendium_group else \
            conf.model_compendium_group

        if uds_path is None:
            logger.error("the UDS path must be set.")
            exit(2)

        if model_interface is None:
            logger.error("the interface code must be set.")
            exit(2)

        conf = GasModelConf(uds_path, model_interface, model_compendium_group)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
