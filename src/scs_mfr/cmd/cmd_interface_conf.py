"""
Created on 27 Feb 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.interface.interface_conf import InterfaceConf
from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdInterfaceConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        models = ' | '.join(InterfaceConf.models())

        self.__parser = optparse.OptionParser(usage="%prog [{ -m MODEL | -d }] [-v]", version=version())

        # optional...
        self.__parser.add_option("--model", "-m", type="string", action="store", dest="model",
                                 help="interface model { %s }" % models)

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the interface configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.set() and self.model is not None and self.model not in InterfaceConf.models():
            return False

        return True


    def set(self):
        return self.model is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


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
        return "CmdInterfaceConf:{source:%s, delete:%s, verbose:%s}" % \
               (self.__opts.source, self.delete, self.verbose)
