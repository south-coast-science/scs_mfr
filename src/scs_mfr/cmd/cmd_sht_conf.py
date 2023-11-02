"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdSHTConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __addr_str(cls, addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [{ [-i INT_ADDR] [-e EXT_ADDR] | -d }] [-v]",
                                              version=version())

        # fields...
        self.__parser.add_option("--int-addr", "-i", type="int", action="store", dest="int_addr",
                                 help="set I2C address of SHT in A4 package")

        self.__parser.add_option("--ext-addr", "-e", type="int", action="store", dest="ext_addr",
                                 help="set I2C address of SHT exposed to air")

        # delete...
        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the SHT configuration")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.set() and self.delete:
            return False

        if self.__args:
            return False

        return True


    def is_complete(self):
        if self.int_addr is None or self.ext_addr is None:
            return False

        return True


    def set(self):
        return self.int_addr is not None or self.ext_addr is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def int_addr(self):
        return self.__opts.int_addr


    @property
    def ext_addr(self):
        return self.__opts.ext_addr


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
        return "CmdSHTConf:{int_addr:%s, ext_addr:%s, delete:%s, verbose:%s}" % \
               (CmdSHTConf.__addr_str(self.int_addr), CmdSHTConf.__addr_str(self.ext_addr),
                self.delete, self.verbose)
