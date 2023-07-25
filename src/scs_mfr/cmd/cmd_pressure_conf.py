"""
Created on 9 Jul 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_core.data.datum import Datum
from scs_dfe.climate.pressure_conf import PressureConf
from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdPressureConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        models = ' | '.join(PressureConf.models())

        self.__parser = optparse.OptionParser(usage="%prog { [-m MODEL] [-a ALTITUDE] | -d } [-v]", version=version())

        # fields...
        self.__parser.add_option("--model", "-m", type="string", action="store", dest="model",
                                 help="barometer model { %s }" % models)

        self.__parser.add_option("--altitude", "-a", type="string", action="store", dest="altitude",
                                 help="altitude in metres or 'GPS' for GPS altitude")

        # delete...
        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the pressure configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if (self.model is not None or self.altitude is not None) and self.delete:
            return False

        if self.altitude is not None and not (self.altitude == 'GPS' or Datum.is_int(self.altitude)):
            return False

        if self.model is not None and self.model not in PressureConf.models():
            return False

        return True


    def set(self):
        return self.altitude or self.model


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def altitude(self):
        try:
            return int(self.__opts.altitude)
        except (TypeError, ValueError):
            return self.__opts.altitude


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
        return "CmdPressureConf:{model:%s, altitude:%s, delete:%s, verbose:%s}" % \
               (self.model, self.altitude, self.delete, self.verbose)
