"""
Created on 2 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdEEPROMWrite(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog FILENAME [-v]", version=version())

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report sent samples to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.filename is None:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def filename(self):
        return self.__args[0] if len(self.__args) > 0 else None


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdEEPROMWrite:{filename:%s, verbose:%s}" % (self.filename, self.verbose)
