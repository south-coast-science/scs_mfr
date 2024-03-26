"""
Created on 9 Aug 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.model.model_map import ModelMap

from scs_mfr import version
from scs_mfr.provision.provision_scs import ProvisionSCS


# --------------------------------------------------------------------------------------------------------------------

class CmdProvisionServiceSCS(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        map_names = ' | '.join(ModelMap.names())
        default_map = ProvisionSCS.default_model_map()

        self.__parser = optparse.OptionParser(usage="%prog [-p ORG GROUP LOCATION [-f]] [-u] [-s] "
                                                    "[{ -a AFE | -d DSI DATE }] [-c] [-b] [-m MODEL_MAP] "
                                                    "[-t TIMEZONE] [-v]", version=version())

        # identity...
        self.__parser.add_option("--project", "-p", type="string", nargs=3, action="store", dest="project",
                                 help="AWS project (LOCATION may be '_')")

        self.__parser.add_option("--force", "-f", action="store_true", dest="force", default=False,
                                 help="do not check for pre-existing topics")

        # operations...
        self.__parser.add_option("--upgrade-pips", "-u", action="store_true", dest="upgrade_pips",
                                 help="upgrade pip and requests")

        self.__parser.add_option("--upgrade-scs", "-s", action="store_true", dest="upgrade_scs",
                                 help="upgrade SCS git repos")

        self.__parser.add_option("--afe-serial", "-a", type="string", action="store", dest="afe_serial",
                                 help="AFE serial number")

        self.__parser.add_option("--dsi", "-d", type="string", nargs=2, action="store", dest="dsi",
                                 help="DSI serial number and YYYY-MM-DD")

        self.__parser.add_option("--co2-scd30", "-c", action="store_true", dest="scd30", default=False,
                                 help="SCD30 is now present")

        self.__parser.add_option("--barometric", "-b", action="store_true", dest="barometric", default=False,
                                 help="ICP is now present")

        self.__parser.add_option("--model-map", "-m", type="string", action="store", dest="model_map",
                                 help="model map { %s } (default %s)" % (map_names, default_map))

        self.__parser.add_option("--timezone", "-t", type="string", action="store", dest="timezone",
                                 help="timezone name")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.afe_serial and self.dsi_serial:
            return False

        if self.__opts.project is None and self.force:
            return False

        if self.__args:
            return False

        return True


    def set_gases(self):
        return self.__opts.afe_serial or self.__opts.dsi or self.scd30


    def electrochems_are_being_set(self):
        return self.__opts.afe_serial or self.__opts.dsi


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def project(self):
        return self.__opts.project is not None


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
    def barometric(self):
        return self.__opts.barometric


    @property
    def model_map(self):
        return self.__opts.model_map


    @property
    def timezone(self):
        return self.__opts.timezone


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdProvisionServiceSCS:{project:%s, force:%s, upgrade_pips:%s, " \
               "afe_serial:%s, dsi:%s, scd30:%s, barometric:%s, model_map:%s, timezone:%s, verbose:%s}" % \
            (self.__opts.project, self.force, self.upgrade_pips,
             self.afe_serial, self.__opts.dsi, self.scd30, self.barometric, self.model_map, self.timezone, self.verbose)
