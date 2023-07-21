"""
Created on 09 Oct 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSIdentity(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s [-g GROUP_NAME] [-c CORE_NAME]] [-i INDENT] [-v]",
                                              version=version())
        # commands...
        self.__parser.add_option("--setup", "-s", action="store_true", dest="setup", default=False,
                                 help="setup the device")

        # optional..
        self.__parser.add_option("--group-name", "-g", action="store", dest="group_name", default=False,
                                 help="Overwrite the name of the group to create")

        self.__parser.add_option("--core-name", "-c", action="store", dest="core_name", default=False,
                                 help="Overwrite the name of the core to create")

        # output...
        self.__parser.add_option("--indent", "-i", action="store", dest="indent", type=int,
                                 help="pretty-print the output with INDENT")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if not self.setup and (bool(self.group_name) or bool(self.core_name)):
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def setup(self):
        return self.__opts.setup


    @property
    def group_name(self):
        return self.__opts.group_name


    @property
    def core_name(self):
        return self.__opts.core_name


    @property
    def indent(self):
        return self.__opts.indent


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAWSIdentity:{setup:%s, group-name:%s, core-name:%s, indent:%s, verbose:%s}" % \
               (self.setup, self.group_name, self.core_name, self.indent, self.verbose)
