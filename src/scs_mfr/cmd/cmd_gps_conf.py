"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.gps.gps_conf import GPSConf
from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdGPSConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ [-m MODEL] [-i INTERVAL] [-t TALLY] [-f REPORT_FILE] "
                                                    "[-l { 0 | 1 }] | -d }] [-v]", version=version())

        # optional...
        self.__parser.add_option("--model", "-m", type="string", action="store", dest="model",
                                 help="set the model (PAM7Q or SAM8Q)")

        self.__parser.add_option("--sample-interval", "-i", type="int", action="store", dest="sample_interval",
                                 help="set sampling interval")

        self.__parser.add_option("--tally", "-t", type="int", action="store", dest="tally",
                                 help="set the averaging tally")

        self.__parser.add_option("--report-file", "-f", type="string", action="store", dest="report_file",
                                 help="file to store latest GPS report")

        self.__parser.add_option("--debug", "-l", type="int", action="store", dest="debug",
                                 help="set debug logging (default is 0)")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the GPS configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.model and not GPSConf.is_valid_model(self.model):
            return False

        return True


    def is_complete(self):
        if self.model is None or self.sample_interval is None or self.tally is None:
            return False

        return True


    def set(self):
        return self.model is not None or self.sample_interval is not None or self.tally is not None or \
               self.report_file is not None or self.__opts.debug is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


    @property
    def sample_interval(self):
        return self.__opts.sample_interval


    @property
    def tally(self):
        return self.__opts.tally


    @property
    def report_file(self):
        return self.__opts.report_file


    @property
    def debug(self):
        return None if self.__opts.debug is None else bool(self.__opts.debug)


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
        return "CmdGPSConf:{model:%s, sample_interval:%s, tally:%s, report_file:%s, debug:%s, delete:%s, " \
               "verbose:%s}" % \
               (self.model, self.sample_interval, self.tally, self.debug, self.report_file, self.delete,
                self.verbose)
