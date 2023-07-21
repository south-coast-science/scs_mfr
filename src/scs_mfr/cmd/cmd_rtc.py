"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdRTC(object):
    """unix command line handler"""

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [-i] [-s] [-v]", version=version())

        # optional...
        self.__parser.add_option("--init", "-i", action="store_true", dest="initialise", default=False,
                                 help="initialise RTC default operating settings")

        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="set RTC time from system time")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def initialise(self):
        return self.__opts.initialise


    @property
    def set(self):
        return self.__opts.set


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdRTC:{initialise:%s, set:%s, verbose:%s}" % (self.initialise, self.set, self.verbose)
