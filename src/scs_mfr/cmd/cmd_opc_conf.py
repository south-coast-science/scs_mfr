"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_dfe.particulate.opc_conf import OPCConf
from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [-n NAME] [{ [-m MODEL] [-s SAMPLE_PERIOD] [-z { 0 | 1 }] "
                                                    "[-p { 0 | 1 }] [-c CUSTOM_DEV_PATH] | -d }] [-v]",
                                              version=version())

        # identity...
        self.__parser.add_option("--name", "-n", type="string", action="store", dest="name",
                                 help="the name of the OPC configuration")

        # fields...
        self.__parser.add_option("--model", "-m", type="string", action="store", dest="model",
                                 help="set MODEL { N2 | N3 | R1 | S30 }")

        self.__parser.add_option("--sample-period", "-s", type="int", action="store", dest="sample_period",
                                 help="set SAMPLE_PERIOD")

        self.__parser.add_option("--restart-on-zeroes", "-z", type="int", dest="restart_on_zeroes",
                                 action="store", help="restart on zero readings (default 1)")

        self.__parser.add_option("--power-saving", "-p", type="int", action="store", dest="power_saving",
                                 help="enable power saving mode (default 0)")

        self.__parser.add_option("--custom-dev-path", "-c", type="string", action="store", dest="custom_dev_path",
                                 help="override default SPI path")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the OPC configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.model and not OPCConf.is_valid_model(self.model):
            return False

        if self.__opts.restart_on_zeroes is not None and \
                not (self.__opts.restart_on_zeroes == 0 or self.__opts.restart_on_zeroes == 1):
            return False

        if self.__opts.power_saving is not None and \
                not (self.__opts.power_saving == 0 or self.__opts.power_saving == 1):
            return False

        return True


    def is_complete(self):
        if self.model is None or self.sample_period is None:
            return False

        return True


    def set(self):
        return self.model is not None or self.sample_period is not None or \
               self.restart_on_zeroes is not None or self.power_saving is not None \
               or self.custom_dev_path is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__opts.name


    @property
    def model(self):
        return self.__opts.model


    @property
    def sample_period(self):
        return self.__opts.sample_period


    @property
    def restart_on_zeroes(self):
        return None if self.__opts.restart_on_zeroes is None else bool(self.__opts.restart_on_zeroes)


    @property
    def power_saving(self):
        return None if self.__opts.power_saving is None else bool(self.__opts.power_saving)


    @property
    def custom_dev_path(self):
        return self.__opts.custom_dev_path


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
        return "CmdOPCConf:{name:%s, model:%s, sample_period:%s, restart_on_zeroes:%s, power_saving:%s, " \
               "custom_dev_path:%s, delete:%s, verbose:%s}" % \
               (self.name, self.model, self.sample_period, self.restart_on_zeroes, self.power_saving,
                self.custom_dev_path, self.delete, self.verbose)
