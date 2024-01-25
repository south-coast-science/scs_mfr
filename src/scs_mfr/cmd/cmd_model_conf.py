"""
Created on 22 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.model.model_mapping import ModelMapping

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdModelConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, interfaces):
        interface_names = ' | '.join(interfaces)
        map_names = ' | '.join(ModelMapping.names())

        self.__parser = optparse.OptionParser(usage="%prog [{ [-u UDS_PATH] [-i INTERFACE] [-m MAP] | -d }] [-v]",
                                              version=version())

        # fields...
        self.__parser.add_option("--uds-path", "-u", type="string", action="store", dest="uds_path",
                                 help="set the UDS path (relative to ~/SCS)")

        self.__parser.add_option("--interface", "-i", type="string", action="store", dest="model_interface",
                                 help="set the interface code { %s }" % interface_names)

        self.__parser.add_option("--model-map", "-m", type="string", action="store", dest="model_map",
                                 help="set the model map { %s }" % map_names)

        # delete...
        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the inference configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.set():
            count += 1

        if self.delete:
            count += 1

        if count > 1:
            return False

        if self.__args:
            return False

        return True


    def is_complete(self):
        if self.uds_path is None or self.model_interface is None or self.model_map is None:
            return False

        return True


    def set(self):
        return self.uds_path is not None or self.model_interface is not None or self.model_map is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def uds_path(self):
        return self.__opts.uds_path


    @property
    def model_interface(self):
        return self.__opts.model_interface


    @property
    def model_map(self):
        return self.__opts.model_map


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
        return "CmdModelConf:{uds_path:%s, model_interface:%s, model_map:%s, delete:%s, verbose:%s}" % \
               (self.uds_path, self.model_interface, self.model_map, self.delete, self.verbose)
