"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdDFETest(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-e] [-g] [-r] [-v] DFE_SERIAL_NUMBER",
                                              version=version())

        # optional...
        self.__parser.add_option("--eeprom", "-e", action="store_true", dest="ignore_eeprom", default=False,
                                 help="ignore EEPROM")

        self.__parser.add_option("--gps", "-g", action="store_true", dest="ignore_gps", default=False,
                                 help="ignore GPS module")

        self.__parser.add_option("--rtc", "-r", action="store_true", dest="ignore_rtc", default=False,
                                 help="ignore real-time clock")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.dfe_serial_number is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def dfe_serial_number(self):
        return self.__args[0] if len(self.__args) > 0 else None


    @property
    def ignore_eeprom(self):
        return self.__opts.ignore_eeprom


    @property
    def ignore_gps(self):
        return self.__opts.ignore_gps


    @property
    def ignore_rtc(self):
        return self.__opts.ignore_rtc


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdDFETest:{dfe_serial_number:%s, ignore_eeprom:%s, ignore_gps:%s, ignore_rtc:%s, verbose:%s}" % \
                    (self.dfe_serial_number, self.ignore_eeprom, self.ignore_gps, self.ignore_rtc, self.verbose)
