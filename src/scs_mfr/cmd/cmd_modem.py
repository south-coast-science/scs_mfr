"""
Created on 30 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdModem(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -m | -c | -s } [-v]", version=version())

        # modem...
        self.__parser.add_option("--model", "-m", action="store_true", dest="model", default=False,
                                 help="report on modem model ")

        self.__parser.add_option("--connection", "-c", action="store_true", dest="connection", default=False,
                                 help="report on modem connection ")

        self.__parser.add_option("--sim", "-s", action="store_true", dest="sim", default=False,
                                 help="report on SIM")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.model:
            count += 1

        if self.connection:
            count += 1

        if self.sim:
            count += 1

        if count != 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


    @property
    def connection(self):
        return self.__opts.connection


    @property
    def sim(self):
        return self.__opts.sim


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdModem:{model:%s, connection:%s, sim:%s, verbose:%s}" % \
               (self.model, self.connection, self.sim, self.verbose)
