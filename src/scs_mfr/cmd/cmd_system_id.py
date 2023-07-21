"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdSystemID(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-d VENDOR_ID] [-m MODEL_ID] [-n MODEL_NAME] [-c CONFIG] "
                                                    "[{-s SYSTEM_SERIAL_NUMBER | -a }] [-v]", version=version())

        # optional...
        self.__parser.add_option("--vendor", "-d", type="string", action="store", dest="vendor_id",
                                 help="set vendor ID")

        self.__parser.add_option("--model", "-m", type="string", action="store", dest="model_id",
                                 help="set model ID")

        self.__parser.add_option("--name", "-n", type="string", action="store", dest="model_name",
                                 help="set model name")

        self.__parser.add_option("--config", "-c", type="string", action="store", dest="configuration",
                                 help="set device configuration")

        self.__parser.add_option("--serial", "-s", type="int", action="store", dest="serial_number",
                                 help="set serial number")

        self.__parser.add_option("--auto-serial", "-a", action="store_true", dest="auto_serial", default=False,
                                 help="set serial number automatically from hostname")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.serial_number is not None and self.auto_serial:
            return False

        return True


    def is_complete(self):
        if self.vendor_id is None or self.model_id is None or self.model_name is None or \
                        self.configuration is None or (self.serial_number is None and not self.auto_serial):
            return False

        return True


    def set(self):
        if self.vendor_id is not None or self.model_id is not None or self.model_name is not None or \
                        self.configuration is not None or self.serial_number is not None or self.auto_serial:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def vendor_id(self):
        return self.__opts.vendor_id


    @property
    def model_id(self):
        return self.__opts.model_id


    @property
    def model_name(self):
        return self.__opts.model_name


    @property
    def configuration(self):
        return self.__opts.configuration


    @property
    def serial_number(self):
        return self.__opts.serial_number


    @property
    def auto_serial(self):
        return self.__opts.auto_serial


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdSystemID:{vendor_id:%s, model_id:%s, model_name:%s, " \
               "configuration:%s, serial_number:%s, auto_serial:%s, verbose:%s}" % \
               (self.vendor_id, self.model_id, self.model_name,
                self.configuration, self.serial_number, self.auto_serial, self.verbose)
