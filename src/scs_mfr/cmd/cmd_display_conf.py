"""
Created on 22 Jun 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.display.display_conf import DisplayConf
from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdDisplayConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ [-m MODE] [-n NAME] [-u STARTUP] [-s SHUTDOWN] "
                                                    "[-t { 1 | 0 }] | -d }] [-v]", version=version())

        # mode...
        self.__parser.add_option("--mode", "-m", type="string", action="store", dest="mode",
                                 help="set display mode (SYS only)")

        self.__parser.add_option("--name", "-n", type="string", action="store", dest="name",
                                 help="set device name")

        self.__parser.add_option("--startup", "-u", type="string", action="store", dest="startup",
                                 help="set startup message")

        self.__parser.add_option("--shutdown", "-s", type="string", action="store", dest="shutdown",
                                 help="set shutdown message")

        self.__parser.add_option("--show-time", "-t", type="int", action="store", dest="show_time",
                                 help="show current time")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete display configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.mode is not None and self.mode not in DisplayConf.modes():
            return False

        return True


    def is_complete(self):
        if self.mode is None or self.device_name is None or \
                self.startup_message is None or self.shutdown_message is None or self.show_time is None:
            return False

        return True


    def set(self):
        return self.mode is not None or self.device_name is not None or \
               self.startup_message is not None or self.shutdown_message is not None or self.show_time is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def mode(self):
        return self.__opts.mode


    @property
    def device_name(self):
        return self.__opts.name


    @property
    def startup_message(self):
        return self.__opts.startup


    @property
    def shutdown_message(self):
        return self.__opts.shutdown


    @property
    def show_time(self):
        return None if self.__opts.show_time is None else bool(self.__opts.show_time)


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
        return "CmdDisplayConf:{mode:%s, device_name:%s, startup_message:%s, shutdown_message:%s, show_time:%s, " \
               "delete:%s, verbose:%s}" % \
               (self.mode, self.device_name, self.startup_message, self.shutdown_message, self.show_time,
                self.delete, self.verbose)
