"""
Created on 24 Nov 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdCognitoDeviceCredentials(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -a INVOICE | -t }] [-v]", version=version())

        # functions...
        self.__parser.add_option("--assert", "-a", type="string", action="store", dest="assert_device",
                                 help="assert the credentials as a Cognito device for INVOICE")

        self.__parser.add_option("--test", "-t", action="store_true", dest="test", default=False,
                                 help="test the credentials")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        # build...
        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def assert_device(self):
        return self.__opts.assert_device is not None


    @property
    def invoice_number(self):
        return self.__opts.assert_device


    @property
    def test(self):
        return self.__opts.test


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdCognitoDeviceCredentials:{assert:%s, test:%s, verbose:%s}" %  \
            (self.__opts.assert_device, self.test, self.verbose)
