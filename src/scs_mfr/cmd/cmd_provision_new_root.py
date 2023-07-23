"""
Created on 24 Feb 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdProvisionNewRoot(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s] [-v]", version=version())

        # operations...
        self.__parser.add_option("--prep-sd", "-s", action="store_true", dest="prep_sd", default=False,
                                 help="format the SD card")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def prep_sd(self):
        return self.__opts.prep_sd


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "CmdProvisionNewRoot:{prep_sd:%s, verbose:%s}" % (self.prep_sd, self.verbose)
