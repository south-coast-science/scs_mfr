"""
Created on 3 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCCleaningInterval(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s INTERVAL] [-v]", version=version())

        # operations...
        self.__parser.add_option("--set", "-s", type="int", action="store", dest="interval",
                                 help="set the cleaning interval (>= 0 seconds)")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.interval is not None and self.interval < 0:
            return False

        if self.__args:
            return False

        return True


    def set(self):
        return self.interval is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def interval(self):
        return self.__opts.interval


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCCleaningInterval:{interval:%s, verbose:%s}" %  (self.interval, self.verbose)
