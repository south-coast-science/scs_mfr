#!/usr/bin/env python3

"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The mqtt_conf utility is not relevant to systems running AWS Greengrass.

The INHIBIT_PUBLISHING field determines whether the MQTT client will publish messages. If inhibit is set to true,
then the client will continue to accept messages and echo these to stdout if required, but will not publish. This
setting is useful when the device is used in an offline mode - in this case data is typically written to a CSV file.

The REPORT_FILE parameter, if set, indicates where the latest queue length value should be stored.

If DEBUG is set to 1 (true), then extra logging will be written to stderr by the MQTT client.

The MQTT client must be restarted for changes to take effect.

WARNING: if inhibit publishing is set to true, the MQTT client will still subscribe as specified, but will not publish
receipts or responses.

SYNOPSIS
mqtt_conf.py { [-i { 0 | 1 }] [-l { 0 | 1 }] | -d } [-v]

EXAMPLES
./mqtt_conf.py -i 0 -l 1

DOCUMENT EXAMPLE
{"inhibit-publishing": false, "debug": true}

FILES
~/SCS/conf/mqtt_conf.json

SEE ALSO
scs_dev/aws_mqtt_client
"""

import sys

from scs_core.comms.mqtt_conf import MQTTConf
from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mqtt_conf import CmdMQTTConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdMQTTConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("mqtt_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    conf = MQTTConf.load(Host, skeleton=True)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        inhibit_publishing = cmd.inhibit_publishing if cmd.inhibit_publishing is not None else conf.inhibit_publishing
        debug = cmd.debug if cmd.debug is not None else conf.debug

        conf = MQTTConf(inhibit_publishing, debug)
        conf.save(Host)

    elif cmd.delete and conf is not None:
        conf.delete(Host)
        conf = None


    if conf:
        print(JSONify.dumps(conf))
