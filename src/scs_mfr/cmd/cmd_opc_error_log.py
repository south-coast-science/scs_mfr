"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCErrorLog(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ -t | -d }] [-i INDENT] [-v]", version=version())

        # functions...
        self.__parser.add_option("--trim", "-t", action="store_true", dest="trim", default=False,
                                 help="trim older entries")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the log")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.trim and self.delete:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def trim(self):
        return self.__opts.trim


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def indent(self):
        return self.__opts.indent


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCErrorLog:{trim:%s, delete:%s, indent:%s, verbose:%s}" % \
               (self.trim, self.delete, self.indent, self.verbose)
