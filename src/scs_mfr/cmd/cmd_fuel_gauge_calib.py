"""
Created on 16 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdFuelGaugeCalib(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { { -c | -d | -l | -r | -z { D | L } } | "
                                                    "{ -f | -s | -g | -p } [-i INTERVAL] } [-v]", version=version())

        # configuration...
        self.__parser.add_option("--gauge-conf", "-c", action="store_true", dest="gauge_conf", default=False,
                                 help="report fuel gauge configuration")

        # single-shot...
        self.__parser.add_option("--dflt-learned", "-d", action="store_true", dest="default_learned", default=False,
                                 help="report battery's default params")

        self.__parser.add_option("--host-learned", "-l", action="store_true", dest="host_learned", default=False,
                                 help="read params from host")

        self.__parser.add_option("--remove-learned", "-r", action="store_true", dest="remove_learned", default=False,
                                 help="delete params from host")

        self.__parser.add_option("--init", "-z", type="string", action="store", dest="init",
                                 help="initialise gauge with configuration and Default or Learned params")

        # iterable...
        self.__parser.add_option("--gauge-learned", "-g", action="store_true", dest="gauge_learned", default=False,
                                 help="read learned params from gauge")

        self.__parser.add_option("--save-learned", "-s", action="store_true", dest="save_learned", default=False,
                                 help="save learned params to host")

        self.__parser.add_option("--fuel", "-f", action="store_true", dest="fuel", default=False,
                                 help="report fuel status")

        self.__parser.add_option("--psu", "-p", action="store_true", dest="psu", default=False,
                                 help="report psu status")

        # output...
        self.__parser.add_option("--interval", "-i", type="int", action="store", dest="interval",
                                 help="sampling interval")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        count = 0

        if self.gauge_conf:
            count += 1

        if self.default_learned:
            count += 1

        if self.host_learned:
            count += 1

        if self.remove_learned:
            count += 1

        if self.init is not None:
            count += 1

        if self.gauge_learned:
            count += 1

        if self.save_learned:
            count += 1

        if self.fuel:
            count += 1

        if self.psu:
            count += 1

        if count != 1:
            return False

        if self.init is not None and self.init != 'D' and self.init != 'L':
            return False

        if self.__opts.interval is not None and not self.gauge_learned and not self.save_learned and \
                not self.fuel and not self.psu:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def gauge_conf(self):
        return self.__opts.gauge_conf


    @property
    def default_learned(self):
        return self.__opts.default_learned


    @property
    def host_learned(self):
        return self.__opts.host_learned


    @property
    def remove_learned(self):
        return self.__opts.remove_learned


    @property
    def init(self):
        return self.__opts.init


    @property
    def gauge_learned(self):
        return self.__opts.gauge_learned


    @property
    def save_learned(self):
        return self.__opts.save_learned


    @property
    def fuel(self):
        return self.__opts.fuel


    @property
    def psu(self):
        return self.__opts.psu


    @property
    def interval(self):
        return 0 if self.__opts.interval is None else self.__opts.interval


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdFuelGaugeCalib:{gauge_conf:%s, default_learned:%s, host_learned:%s, remove_learned:%s, init:%s, " \
               "gauge_learned:%s, save_learned:%s, fuel:%s, psu:%s, interval:%s, verbose:%s}" % \
               (self.gauge_conf, self.default_learned, self.host_learned, self.remove_learned, self.init,
                self.gauge_learned, self.save_learned, self.fuel, self.psu, self.__opts.interval, self.verbose)
