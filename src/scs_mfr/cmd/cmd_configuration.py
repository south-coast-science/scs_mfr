"""
Created on 29 Jan 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdConfiguration(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s CONFIGURATION] [-x] [{ -i INDENT | -t }] [-v]",
                                              version=version())

        # mode...
        self.__parser.add_option("--save", "-s", type="string", action="store", dest="configuration",
                                 help="save the given JSON configuration component(s)")

        # output...
        self.__parser.add_option("--exclude-sim", "-x", action="store_true", dest="exclude_sim", default=False,
                                 help="exclude SIM information from output")

        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--table", "-t", action="store_true", dest="table", default=False,
                                 help="output in comma-separated format")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.indent and self.table:
            return False

        return True


    def save(self):
        return self.__opts.configuration is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def configuration(self):
        return self.__opts.configuration


    @property
    def exclude_sim(self):
        return self.__opts.exclude_sim


    @property
    def indent(self):
        return self.__opts.indent


    @property
    def table(self):
        return self.__opts.table


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdConfiguration:{configuration:%s, exclude_sim:%s, indent:%s, table:%s, verbose:%s}" % \
               (self.configuration, self.exclude_sim, self.indent, self.table, self.verbose)
