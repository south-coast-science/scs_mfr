"""
Created on 8 Sep 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# TODO: sort out flag syntax
# --------------------------------------------------------------------------------------------------------------------

class CmdSCD30Conf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ [-i INTERVAL] [-t OFFSET] | -d }] [-v]",
                                              version=version())

        # optional...
        self.__parser.add_option("--sample-interval", "-i", type="int", dest="sample_interval",
                                 action="store", help="set the SCD30 sample interval")

        self.__parser.add_option("--temp-offset", "-t", type="float", dest="temperature_offset",
                                 action="store", help="set the temperature offset")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the SCD30 configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.sample_interval is not None and self.delete:
            return False

        return True


    def is_complete(self):
        if self.sample_interval is None or self.temperature_offset is None:
            return False

        return True


    def set(self):
        return self.__opts.sample_interval is not None or self.__opts.temperature_offset is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sample_interval(self):
        return self.__opts.sample_interval


    @property
    def temperature_offset(self):
        return self.__opts.temperature_offset


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
        return "CmdSCD30Conf:{sample_interval:%s, temperature_offset:%s, delete:%s, verbose:%s}" % \
                    (self.sample_interval, self.temperature_offset, self.delete, self.verbose)
