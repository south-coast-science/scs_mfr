"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version
from scs_psu.psu.psu_conf import PSUConf


# --------------------------------------------------------------------------------------------------------------------

class CmdPSUConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        psu_models = ' | '.join(PSUConf.psu_models())
        batt_models = ' | '.join(PSUConf.batt_models())

        self.__parser = optparse.OptionParser(usage="%prog { [-p PSU_MODEL] [-b BATT_MODEL] [-t { 1 | 0 }] "
                                                    "[-i REPORTING_INTERVAL] [-f REPORT_FILE] | -d } [-v]",
                                              version=version())

        # optional...
        self.__parser.add_option("--psu-model", "-p", type="string", action="store", dest="psu_model",
                                 help="set PSU model { %s }" % psu_models)

        self.__parser.add_option("--batt-model", "-b", type="string", action="store", dest="batt_model",
                                 help="set battery model { %s }" % batt_models)

        self.__parser.add_option("--ignore-threshold", "-t", type="int", action="store",
                                 dest="ignore_threshold", help="ignore power threshold (default false)")

        self.__parser.add_option("--reporting-interval", "-i", type="int", action="store",
                                 dest="reporting_interval", help="PSU monitor reporting interval")

        self.__parser.add_option("--report-file", "-f", type="string", action="store", dest="report_file",
                                 help="PSU monitor status report file")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the PSU configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.delete and \
                (self.psu_model is not None or self.batt_model is not None or self.ignore_threshold is not None or
                 self.reporting_interval is not None or self.report_file is not None):
            return False

        if self.psu_model is not None and self.psu_model not in PSUConf.psu_models():
            return False

        if self.batt_model is not None and self.batt_model not in PSUConf.batt_models():
            return False

        return True


    def set(self):
        return self.__opts.psu_model is not None or self.__opts.batt_model is not None or \
               self.__opts.ignore_threshold is not None or self.__opts.reporting_interval is not None or \
               self.__opts.report_file is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def psu_model(self):
        return self.__opts.psu_model


    @property
    def batt_model(self):
        return self.__opts.batt_model


    @property
    def ignore_threshold(self):
        return None if self.__opts.ignore_threshold is None else bool(self.__opts.ignore_threshold)


    @property
    def reporting_interval(self):
        return self.__opts.reporting_interval


    @property
    def report_file(self):
        return self.__opts.report_file


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
        return "CmdPSUConf:{psu_model:%s, batt_model:%s, ignore_threshold:%s, reporting_interval:%s, " \
               "report_file:%s, delete:%s, verbose:%s}" % \
               (self.psu_model, self.batt_model, self.ignore_threshold, self.reporting_interval,
                self.report_file, self.delete, self.verbose)
