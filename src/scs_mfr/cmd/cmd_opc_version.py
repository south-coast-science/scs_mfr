"""
Created on 17 May 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCVersion(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-n NAME] [{ -s | -d }] [-v]", version=version())

        # identity...
        self.__parser.add_option("--name", "-n", type="string", action="store", dest="name",
                                 help="the name of the OPC")

        # function...
        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="read from OPC and save to file")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the file")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.set:
            count += 1

        if self.delete:
            count += 1

        if count > 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__opts.name


    @property
    def set(self):
        return self.__opts.set


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCVersion:{name:%s, set:%s, delete:%s, verbose:%s}" % \
               (self.name, self.set, self.delete, self.verbose)
