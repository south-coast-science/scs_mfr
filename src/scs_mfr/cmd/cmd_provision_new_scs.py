"""
Created on 14 Jul 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.model.model_map import ModelMap

from scs_mfr import version
from scs_mfr.provision.provision_scs import ProvisionSCS

from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

class CmdProvisionNewSCS(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        psu_models = ' | '.join(PSUConf.psu_models())
        map_names = ' | '.join(ModelMap.names())
        default_map = ProvisionSCS.default_model_map()

        self.__parser = optparse.OptionParser(usage="%prog -i INVOICE -p ORG GROUP LOCATION [-f] [-g DEVICE_GENUS] "
                                                    "[-u] [{ -a AFE | -d DSI DATE }] [-c] [-s PSU_MODEL] "
                                                    "[-m MODEL_MAP] [-t TIMEZONE] [-x] [-v]", version=version())

        # identity...
        self.__parser.add_option("--invoice-number", "-i", type="string", action="store", dest="invoice_number",
                                 help="invoice number")

        self.__parser.add_option("--project", "-p", type="string", nargs=3, action="store", dest="project",
                                 help="AWS project (LOCATION may be '_')")

        self.__parser.add_option("--force", "-f", action="store_true", dest="force", default=False,
                                 help="do not check for pre-existing topics")

        self.__parser.add_option("--device-genus", "-g", type="string", action="store", dest="device_genus",
                                 help="device group / model")

        # operations...
        self.__parser.add_option("--upgrade-pips", "-u", action="store_true", dest="upgrade_pips",
                                 help="upgrade pip and requests")

        self.__parser.add_option("--afe-serial", "-a", type="string", action="store", dest="afe_serial",
                                 help="AFE serial number")

        self.__parser.add_option("--dsi", "-d", type="string", nargs=2, action="store", dest="dsi",
                                 help="DSI serial number and YYYY-MM-DD")

        self.__parser.add_option("--co2-scd30", "-c", action="store_true", dest="scd30", default=False,
                                 help="SCD30 is present")

        self.__parser.add_option("--psu-model", "-s", type="string", action="store", dest="psu_model",
                                 help="PSU model { %s }" % psu_models)

        self.__parser.add_option("--model-map", "-m", type="string", action="store", dest="model_map",
                                 help="model map { %s } (default %s)" % (map_names, default_map))

        self.__parser.add_option("--timezone", "-t", type="string", action="store", dest="timezone",
                                 help="timezone name")

        # output...
        self.__parser.add_option("--exclude-tests", "-x", action="store_true", dest="exclude_test", default=False,
                                 help="do not perform OS checks or hardware tests")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.invoice_number is None or self.__opts.project is None:
            return False

        if self.__opts.project is None and self.force:
            return False

        if self.afe_serial and self.dsi_serial:
            return False

        if self.__args:
            return False

        return True


    def has_gases(self):
        return self.__opts.afe_serial or self.__opts.dsi or self.scd30


    def electrochems_are_being_set(self):
        return self.__opts.afe_serial or self.__opts.dsi


    # ----------------------------------------------------------------------------------------------------------------
    # properties: identity...

    @property
    def invoice_number(self):
        return self.__opts.invoice_number


    @property
    def project_org(self):
        return None if self.__opts.project is None else self.__opts.project[0]


    @property
    def project_group(self):
        return None if self.__opts.project is None else self.__opts.project[1]


    @property
    def project_location(self):
        return None if self.__opts.project is None else self.__opts.project[2]


    @property
    def force(self):
        return self.__opts.force


    @property
    def device_genus(self):
        return self.__opts.device_genus


    # ----------------------------------------------------------------------------------------------------------------
    # properties: operations...

    @property
    def upgrade_pips(self):
        return self.__opts.upgrade_pips


    @property
    def afe_serial(self):
        return self.__opts.afe_serial


    @property
    def dsi_serial(self):
        return self.__opts.dsi[0] if self.__opts.dsi else None


    @property
    def dsi_calibration_date(self):
        return self.__opts.dsi[1] if self.__opts.dsi else None


    @property
    def scd30(self):
        return self.__opts.scd30


    @property
    def psu_model(self):
        return self.__opts.psu_model


    @property
    def model_map(self):
        return self.__opts.model_map


    @property
    def timezone(self):
        return self.__opts.timezone


    # ----------------------------------------------------------------------------------------------------------------
    # properties: output...

    @property
    def exclude_test(self):
        return self.__opts.exclude_test


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdProvisionNewSCS:{invoice_number:%s, project:%s, force:%s, device_genus:%s, upgrade_pips:%s, " \
               "afe_serial:%s, dsi:%s, scd30:%s, psu_model:%s, model_map:%s, timezone:%s, " \
                "exclude_test:%s, verbose:%s}" % \
            (self.invoice_number, self.__opts.project, self.force, self.device_genus, self.upgrade_pips,
             self.afe_serial, self.__opts.dsi, self.scd30, self.psu_model, self.model_map, self.timezone,
             self.exclude_test, self.verbose)
