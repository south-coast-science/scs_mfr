"""
Created on 2 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdSCD30Baseline(object):
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
        self.__parser = optparse.OptionParser(usage="%prog [{ { { -s | -o } VALUE | -c CORRECT REPORTED } "
                                                    "[-t TEMP -m HUMID [-p PRESS]] | -z  | -d }] [-v]",
                                              version=version())

        # fields...
        self.__parser.add_option("--set", "-s", type="int", action="store", dest="set",
                                 help="set offset to integer VALUE")

        self.__parser.add_option("--offset", "-o", type="int", action="store", dest="offset",
                                 help="change offset by integer VALUE")

        self.__parser.add_option("--correct", "-c", type="int", nargs=2, action="store", dest="correct",
                                 help="change offset by the difference between CORRECT and REPORTED values")

        self.__parser.add_option("--zero", "-z", action="store_true", dest="zero",
                                 help="zero all offsets")

        # delete...
        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the baseline configuration")

        # sample...
        self.__parser.add_option("--temp", "-t", type="float", action="store", dest="temp",
                                 help="record temperature value (°C)")

        self.__parser.add_option("--humid", "-m", type="float", action="store", dest="humid",
                                 help="record relative humidity value (%)")

        self.__parser.add_option("--press", "-p", type="float", action="store", dest="press",
                                 help="record actual barometric pressure value (kPa)")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        param_count = 0

        # setters...
        if self.__opts.set is not None:
            param_count += 1

        if self.__opts.offset is not None:
            param_count += 1

        if self.__opts.correct is not None:
            param_count += 1

        if self.zero is not None:
            param_count += 1

        if self.delete:
            param_count += 1

        if param_count > 1:
            return False

        # environment...
        if bool(self.humid is None) != bool(self.temp is None):
            return False

        if self.__args:
            return False

        return True


    def env_is_specified(self):
        return self.humid is not None and self.temp is not None


    # ----------------------------------------------------------------------------------------------------------------

    def update(self):
        return self.__opts.set or self.__opts.offset or self.__opts.correct


    def has_sample(self):
        return self.__opts.temp is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def set_value(self):
        return self.__opts.set


    @property
    def offset_value(self):
        return self.__opts.offset


    @property
    def correct_value(self):
        return int(self.__opts.correct[0]) if self.__opts.correct else None


    @property
    def reported_value(self):
        return int(self.__opts.correct[1]) if self.__opts.correct else None


    @property
    def temp(self):
        return self.__opts.temp


    @property
    def humid(self):
        return self.__opts.humid


    @property
    def press(self):
        return self.__opts.press


    @property
    def zero(self):
        return self.__opts.zero


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
        return "CmdSCD30Baseline:{set:%s, offset:%s, correct:%s, temp:%s, humid:%s, press:%s, zero:%s, " \
               "delete:%s, indent:%s, verbose:%s}" % \
               (self.set_value, self.offset_value, self.__opts.correct, self.temp, self.humid, self.press, self.zero,
                self.delete, self.indent, self.verbose)
