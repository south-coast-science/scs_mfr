"""
Created on 29 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdSchedule(object):
    """unix command line handler"""

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{-s NAME INTERVAL TALLY | -r NAME }] [-v]",
                                              version=version())

        # optional...
        self.__parser.add_option("--set", "-s", type="string", nargs=3, action="store", dest="set",
                                 help="set schedule NAME, INTERVAL (seconds) and TALLY (count)")

        self.__parser.add_option("--remove", "-r", type="string", action="store", dest="remove",
                                 help="remove the named schedule")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.remove():
            return False

        if self.set():
            try:
                float(self.__opts.set[1])
                int(self.__opts.set[2])

            except ValueError:
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.__opts.set is not None


    def remove(self):
        return self.__opts.remove is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        if self.__opts.set is not None:
            return self.__opts.set[0]

        if self.__opts.remove is not None:
            return self.__opts.remove

        return None


    @property
    def interval(self):
        return None if self.__opts.set is None else self.__opts.set[1]


    @property
    def count(self):
        return None if self.__opts.set is None else self.__opts.set[2]


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdSchedule:{set:%s, remove:%s, verbose:%s}" % \
                    (self.__opts.set, self.__opts.remove, self.verbose)
