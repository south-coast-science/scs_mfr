"""
Created on 13 Feb 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCFirmwareConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [-n NAME] [{ -s FIELD VALUE | -f CONF_FILE }] [-c] [-v]",
                                              version=version())

        # optional...
        self.__parser.add_option("--name", "-n", type="string", action="store", dest="name",
                                 help="the name of the OPC configuration")

        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set FIELD to numeric VALUE")

        self.__parser.add_option("--file", "-f", type="string", action="store", dest="file",
                                 help="load the named CONF_FILE")

        self.__parser.add_option("--commit", "-c", action="store_true", dest="commit", default=False,
                                 help="commit the configuration to non-volatile memory")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.set is not None and self.file is not None:
            return False

        if self.__opts.set is not None:
            try:
                float(self.__opts.set[1])
            except ValueError:
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__opts.name


    @property
    def set_field(self):
        return None if self.__opts.set is None else self.__opts.set[0]


    @property
    def set_value(self):
        return None if self.__opts.set is None else float(self.__opts.set[1])


    @property
    def file(self):
        return self.__opts.file


    @property
    def commit(self):
        return self.__opts.commit


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCConf:{name:%s, set:%s, file:%s, commit:%s, verbose:%s}" % \
               (self.name, self.__opts.set, self.__opts.file, self.__opts.commit, self.verbose)
