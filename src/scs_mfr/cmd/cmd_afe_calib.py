"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from datetime import date

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdAFECalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -f SERIAL_NUMBER | -a SERIAL_NUMBER | "
                                                    "-s SERIAL_NUMBER YYYY-MM-DD | -r | -t  | -d }] [-i INDENT] [-v]",
                                              version=version())

        # operations...
        self.__parser.add_option("--find", "-f", type="string", action="store", dest="find_serial_number",
                                 help="find calibration data (without loading it)")

        self.__parser.add_option("--afe", "-a", type="string", action="store", dest="afe_serial_number",
                                 help="load calibration data for AFE with serial number")

        self.__parser.add_option("--sensor", "-s", type="string", nargs=2, action="store", dest="sensor",
                                 help="load calibration data for DSI with serial number and calibration date")

        self.__parser.add_option("--reload", "-r", action="store_true", dest="reload", default=False,
                                 help="reload calibration data")

        self.__parser.add_option("--test", "-t", action="store_true", dest="test", default=False,
                                 help="set AFE as test load")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete this calibration")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.find_serial_number is not None:
            count += 1

        if self.afe_serial_number is not None:
            count += 1

        if self.sensor is not None:
            count += 1

        if self.reload:
            count += 1

        if self.test:
            count += 1

        if self.delete:
            count += 1

        if count > 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.afe_serial_number is not None or self.sensor is not None


    def update(self):
        return self.afe_serial_number is not None or self.sensor is not None or self.reload or self.test


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def find_serial_number(self):
        return self.__opts.find_serial_number


    @property
    def afe_serial_number(self):
        return self.__opts.afe_serial_number


    @property
    def sensor(self):
        return self.__opts.sensor


    @property
    def sensor_serial_number(self):
        return None if self.__opts.sensor is None else self.__opts.sensor[0]


    @property
    def sensor_calibration_date_str(self):
        return None if self.__opts.sensor is None else self.__opts.sensor[1]


    @property
    def sensor_calibration_date(self):
        if self.__opts.sensor is None:
            return None

        pieces = self.__opts.sensor[1].split('-')
        return date(int(pieces[0]), int(pieces[1]), int(pieces[2]))


    @property
    def reload(self):
        return self.__opts.reload


    @property
    def test(self):
        return self.__opts.test


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
        return "CmdAFECalib:{find_serial_number:%s, afe_serial_number:%s, sensor:%s, reload:%s, test:%s, delete:%s, " \
               "indent:%s, verbose:%s}" % \
               (self.find_serial_number, self.afe_serial_number, self.sensor, self.reload, self.test, self.delete,
                self.indent, self.verbose)
