"""
Created on 12 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdTimezone(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ -z | -s TIMEZONE_NAME | -l }] [-v]",
                                              version=version())

        # helper...
        self.__parser.add_option("--zones", "-z", action="store_true", dest="list", default=False,
                                 help="list the available timezone names to stderr")

        # operations...
        self.__parser.add_option("--set", "-s", type="string", action="store", dest="zone",
                                 help="override system timezone with ZONE")

        self.__parser.add_option("--link", "-l", action="store_true", dest="link", default=False,
                                 help="link to system timezone")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if int(self.list) + int(bool(self.zone)) + int(self.link) > 1:
            return False

        return True


    def set(self):
        return self.zone is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def list(self):
        return self.__opts.list


    @property
    def zone(self):
        return self.__opts.zone


    @property
    def link(self):
        return self.__opts.link


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdTimezone:{list:%s, zone:%s, link:%s, verbose:%s}" % (self.list, self.zone, self.link, self.verbose)
