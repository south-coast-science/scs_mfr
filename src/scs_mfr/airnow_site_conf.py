#!/usr/bin/env python3

"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The airnow_site_conf utility is used to set the site code and any parameter occurrence codes associated with the
AirNow-I project. If available, the configuration is published by the scs_dev/status_sampler utility.

For remote configuration, the airnow_site_conf utility should be made accessible via the
scs_dev/control_receiver.

The utility can be used to list the available countries and AQCSV parameter codes.

SYNOPSIS
airnow_site_conf.py { -c | -p | [-s COUNTRY LOCATION IS_MOBILE] [-o PARAM POC] [-d PARAM] } [-v]

EXAMPLES
./airnow_site_conf.py -s 850 123456789 1 -v

FILES
~/SCS/aws/airnow_site_conf.json

DOCUMENT EXAMPLE
{"site": "850MM123456789", "pocs": {"88102": 2}}

SEE ALSO
scs_analysis/aws_mqtt_control
scs_dev/control_receiver
scs_dev/status_sampler

RESOURCES
https://www.airnow.gov/
"""

import sys

from scs_core.aqcsv.conf.airnow_site_conf import AirNowSiteConf

from scs_core.aqcsv.specification.country_iso import CountryISO
from scs_core.aqcsv.specification.country_numeric import CountryNumeric
from scs_core.aqcsv.specification.parameter import Parameter

from scs_core.aqcsv.data.aqcsv_site import AQCSVSite

from scs_core.data.json import JSONify

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_airnow_site_conf import CmdAirNowSiteConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAirNowSiteConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print("airnow_site_conf: %s" % cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    conf = AirNowSiteConf.load(Host)

    if cmd.verbose and conf is not None:
        print("airnow_site_conf: %s" % conf, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    # countries...
    if cmd.countries:
        for iso in sorted(CountryISO.keys()):
            country = CountryISO.instance(iso)
            print("%s\t%03d\t%s" % (country.iso, country.numeric, country.name))

        exit(0)

    # parameters...
    if cmd.parameters:
        for code in sorted(Parameter.keys()):
            parameter = Parameter.instance(code)
            print("%05d\t%s" % (parameter.code, parameter.description))

        exit(0)

    # set site...
    if cmd.is_set_site():
        if cmd.site_country_code not in CountryNumeric.keys():
            print("airnow_site_conf: country code '%s' is not recognised." % cmd.site_country_code,
                  file=sys.stderr)
            exit(2)

        length = AQCSVSite.LOCATION_CODE_LENGTH

        if len(str(cmd.site_location_code)) != length:
            print("airnow_site_conf: location code '%s' must be %d digits." % (cmd.site_location_code, length),
                  file=sys.stderr)
            exit(2)

        site = AQCSVSite(cmd.site_country_code, cmd.site_location_code, cmd.site_is_mobile)

        pocs = {} if conf is None else conf.pocs

        conf = AirNowSiteConf(site, pocs)
        conf.save(Host)

    # set poc...
    if cmd.is_set_poc():
        if cmd.poc_parameter_code not in Parameter.keys():
            print("airnow_site_conf: parameter code '%s' is not recognised." % cmd.poc_parameter_code,
                  file=sys.stderr)
            exit(2)

        site = None if conf is None else conf.site
        pocs = {} if conf is None else conf.pocs

        pocs[str(cmd.poc_parameter_code)] = cmd.poc_code

        conf = AirNowSiteConf(site, pocs)
        conf.save(Host)

    # delete poc...
    if cmd.is_delete_poc():
        if cmd.poc_delete not in Parameter.keys():
            print("airnow_site_conf: parameter code '%s' is not recognised." % cmd.poc_delete,
                  file=sys.stderr)
            exit(2)

        site = None if conf is None else conf.site
        pocs = {} if conf is None else conf.pocs

        try:
            del pocs[str(cmd.poc_delete)]
        except KeyError:
            pass

        conf = AirNowSiteConf(site, pocs)
        conf.save(Host)

    # report...
    if conf:
        print(JSONify.dumps(conf))
