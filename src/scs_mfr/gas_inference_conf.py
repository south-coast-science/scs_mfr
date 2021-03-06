#!/usr/bin/env python3

"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The gas_inference_conf utility is used to specify how Greengrass data interpretation models are to be accessed:

* UDS_PATH - the Unix domain socket for communication between the gas sampler and the inference server
* INTERFACE - the format of the request
* SPECIES: RESOURCE_NAME - the model resource for each gas

The gases_sampler and Greengrass container must be restarted for changes to take effect.

SYNOPSIS
gas_inference_conf.py [{ [-u UDS_PATH] [-i INTERFACE] | -d }] [-v]

EXAMPLES
./gas_inference_conf.py -u pipes/lambda-gas-model.uds -i vB -v

DOCUMENT EXAMPLE
{"uds-path": "pipes/lambda-gas-model.uds", "model-interface": "vB"}

FILES
~/SCS/conf/gas_model_conf.json

SEE ALSO
scs_dev/gases_sampler
"""

import sys

from scs_core.data.json import JSONify
from scs_core.model.gas.gas_model_conf import GasModelConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_inference_conf import CmdInferenceConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdInferenceConf(GasModelConf.interfaces())

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("gas_inference_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # GasModelConf...
    conf = GasModelConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            print("gas_inference_conf: No configuration is stored - you must therefore set both fields.",
                  file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(2)

        uds_path = cmd.uds_path if cmd.uds_path else conf.uds_path
        model_interface = cmd.model_interface if cmd.model_interface else conf.model_interface

        conf = GasModelConf(uds_path, model_interface)
        conf.save(Host)

    if cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None

    if conf:
        print(JSONify.dumps(conf))
