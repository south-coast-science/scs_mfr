"""
Created on 24 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdProvisionNewSCS(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog -i INVOICE -p ORG GROUP LOCATION [{ -a AFE | -d DSI DATE }] "
                                                    "[-s] [-t] [-v]", version="%prog 1.0")

        # required settings...
        self.__parser.add_option("--invoice-number", "-i", type="string", action="store", dest="invoice_number",
                                 help="invoice number")

        self.__parser.add_option("--project", "-p", type="string", nargs=3, action="store", dest="project",
                                 help="DSI serial number and date")

        # optional settings...
        self.__parser.add_option("--afe-serial", "-a", type="string", action="store", dest="afe_serial",
                                 help="AFE serial number")

        self.__parser.add_option("--dsi", "-d", type="string", nargs=2, action="store", dest="dsi",
                                 help="DSI serial number and date")

        self.__parser.add_option("--scd30", "-s", action="store_true", dest="scd30", default=False,
                                 help="SCD30 is present")

        self.__parser.add_option("--timezone", "-t", type="string", action="store", dest="timezone",
                                 help="timezone name")

        # narrative...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.invoice_number is None or self.__opts.project is None:
            return False

        if self.afe_serial and self.dsi_serial:
            return False

        return True


    def has_gases(self):
        return self.__opts.afe_serial or self.__opts.dsi or self.scd30


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def invoice_number(self):
        return self.__opts.invoice_number


    @property
    def project_org(self):
        return self.__opts.project[0] if self.__opts.project else None


    @property
    def project_group(self):
        return self.__opts.project[1] if self.__opts.project else None


    @property
    def project_location(self):
        return self.__opts.project[2] if self.__opts.project else None


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
    def timezone(self):
        return self.__opts.timezone


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdProvisionNewSCS:{invoice_number:%s, project:%s, afe_serial:%s, dsi:%s, scd30:%s, timezone:%s, " \
               "verbose:%s}" % \
            (self.__opts.project, self.invoice_number, self.afe_serial, self.__opts.dsi, self.scd30, self.timezone,
             self.verbose)
