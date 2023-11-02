"""
Created on 10 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.data.datetime import LocalizedDatetime
from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdVCalBaseline(object):
    """unix command line handler"""


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def __is_integer(value):
        try:
            int(value)
        except ValueError:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -b GAS  | { { -s | -o } GAS VALUE "
                                                    "[-r SAMPLE_REC -t SAMPLE_TEMP -m SAMPLE_HUMID] } "
                                                    "| -d }] [-i INDENT] [-v]", version=version())

        # operations...
        self.__parser.add_option("--baseline", "-b", type="string", action="store", dest="baseline",
                                 help="report offset for GAS")

        self.__parser.add_option("--set", "-s", type="string", nargs=2, action="store", dest="set",
                                 help="set offset for GAS to integer VALUE")

        self.__parser.add_option("--offset", "-o", type="string", nargs=2, action="store", dest="offset",
                                 help="change offset for GAS, by integer VALUE")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the baseline configuration")

        # sample...
        self.__parser.add_option("--sample-rec", "-r", type="string", action="store", dest="sample_rec",
                                 help="sample ISO 8601 datetime")

        self.__parser.add_option("--sample-temp", "-t", type="float", action="store", dest="sample_temp",
                                 help="sample temperature")

        self.__parser.add_option("--sample-humid", "-m", type="float", action="store", dest="sample_humid",
                                 help="sample humidity")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        # commands...
        if self.baseline is not None:
            count += 1

        if self.set is not None:
            count += 1

        if self.offset is not None:
            count += 1

        if self.delete:
            count += 1

        if count > 1:
            return False

        # sample...
        count = 0

        if self.__opts.sample_rec is not None:
            count += 1

        if self.__opts.sample_temp is not None:
            count += 1

        if self.__opts.sample_humid is not None:
            count += 1

        if count != 0 and count != 3:
            return False

        if count == 3 and self.set is None and self.offset is None:
            return False

        # VALUE...
        if self.set is not None and not self.__is_integer(self.set[1]):
            return False

        if self.offset is not None and not self.__is_integer(self.offset[1]):
            return False

        if self.__args:
            return False

        return True


    def is_valid_sample_rec(self):
        if self.__opts.sample_rec is None:
            return True

        return self.sample_rec is not None


    # ----------------------------------------------------------------------------------------------------------------

    def gas_name(self):
        if self.baseline:
            return self.baseline

        if self.set:
            return self.set[0]

        if self.offset:
            return self.offset[0]

        return None


    def update(self):
        return self.set is not None or self.offset is not None


    def has_sample(self):
        return self.__opts.sample_rec is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def baseline(self):
        return self.__opts.baseline


    @property
    def set(self):
        return self.__opts.set


    def set_value(self):
        return None if self.set is None else int(self.set[1])


    @property
    def offset(self):
        return self.__opts.offset


    def offset_value(self):
        return int(self.offset[1]) if self.offset else None


    @property
    def delete(self):
        return self.__opts.delete


    @property
    def sample_rec(self):
        return LocalizedDatetime.construct_from_iso8601(self.__opts.sample_rec)


    @property
    def sample_temp(self):
        return self.__opts.sample_temp


    @property
    def sample_humid(self):
        return self.__opts.sample_humid


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
        return "CmdVCalBaseline:{baseline:%s, set:%s, offset:%s, delete:%s, " \
               "sample_rec:%s, sample_temp:%s, sample_humid:%s, indent:%s, verbose:%s}" % \
               (self.baseline, self.set, self.offset, self.delete,
                self.sample_rec, self.sample_temp, self.sample_humid, self.indent, self.verbose)
