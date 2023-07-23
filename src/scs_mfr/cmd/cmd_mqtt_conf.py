"""
Created on 17 May 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdMQTTConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog { [-i { 0 | 1 }] [-f REPORT_FILE] [-l { 0 | 1 }] | "
                                                    "-d } [-v]", version=version())

        # fields...
        self.__parser.add_option("--inhibit-pub", "-i", type="int", action="store", dest="inhibit_publishing",
                                 default=None, help="inhibit publishing (1) or enable (0)")

        self.__parser.add_option("--report-file", "-f", type="string", action="store", dest="report_file",
                                 help="file to store latest queue length value")

        self.__parser.add_option("--debug", "-l", type="int", action="store", dest="debug",
                                 help="set debug logging (default is 0)")

        # delete...
        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="revert to the default MQTT configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.__opts.debug is not None and self.__opts.debug != 0 and self.__opts.debug != 1:
            return False

        if self.__opts.inhibit_publishing is not None and self.__opts.inhibit_publishing not in (0, 1):
            return False

        return True


    def set(self):
        return self.inhibit_publishing is not None or self.report_file is not None or self.__opts.debug is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def inhibit_publishing(self):
        return self.__opts.inhibit_publishing


    @property
    def report_file(self):
        return self.__opts.report_file


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def debug(self):
        return None if self.__opts.debug is None else bool(self.__opts.debug)


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdMQTTConf:{inhibit_publishing:%s, report_file:%s, debug:%s, delete:%s, verbose:%s}" % \
               (self.inhibit_publishing, self.report_file, self.debug, self.delete, self.verbose)
