"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdInferenceConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interfaces):
        self.__interfaces = interfaces
        interface_names = ' | '.join(interfaces)

        self.__parser = optparse.OptionParser(usage="%prog [{ [-u UDS_PATH] [-i INTERFACE] | -d }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--uds-path", "-u", type="string", nargs=1, action="store", dest="uds_path",
                                 help="set the UDS path (relative to ~/SCS)")

        self.__parser.add_option("--interface", "-i", type="string", nargs=1, action="store", dest="model_interface",
                                 help="set the interface code { %s }" % interface_names)

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the inference configuration")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.model_interface and self.model_interface not in self.__interfaces:
            return False

        return True


    def is_complete(self):
        if self.uds_path is None or self.model_interface is None:
            return False

        return True


    def set(self):
        return self.uds_path is not None or self.model_interface is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def uds_path(self):
        return self.__opts.uds_path


    @property
    def model_interface(self):
        return self.__opts.model_interface


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
        return "CmdInferenceConf:{uds_path:%s, model_interface:%s, delete:%s, verbose:%s}" % \
               (self.uds_path, self.model_interface, self.delete, self.verbose)
