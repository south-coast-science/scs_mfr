"""
Created on 2 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example document:
{"org-id": "south-coast-science-test-user", "api-key": "9fdfb841-3433-45b8-b223-3f5a283ceb8e"}
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdSharedSecret(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [{ -g [-i] | -d }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--generate", "-g", action="store_true", dest="generate", default=False,
                                 help="set shared secret")

        self.__parser.add_option("--ignore-credentials", "-i", action="store_true", dest="ignore_credentials",
                                 default=False, help="do not attempt to update credentials")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the shared secret")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.generate and self.delete:
            return False

        if self.ignore_credentials and not self.generate:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def generate(self):
        return self.__opts.generate


    @property
    def ignore_credentials(self):
        return self.__opts.ignore_credentials


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
        return "CmdSharedSecret:{generate:%s, ignore_credentials:%s, delete:%s, verbose:%s}" % \
               (self.generate, self.ignore_credentials, self.delete, self.verbose)
