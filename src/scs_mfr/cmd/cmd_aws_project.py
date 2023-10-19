"""
Created on 3 Apr 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdAWSProject(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s ORG GROUP LOCATION [-f]] [-d] [-v]",
                                              version=version())

        # operations...
        self.__parser.add_option("--set", "-s", type="string", nargs=3, action="store", dest="project",
                                 help="set project specification")

        self.__parser.add_option("--force", "-f", action="store_true", dest="force", default=False,
                                 help="do not check for pre-existing topics")

        self.__parser.add_option("--delete", "-d", action="store_true", dest="delete", default=False,
                                 help="delete the project reference")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()




    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.force and self.__opts.project is None:
            return False

        if self.__args:
            return False

        return True


    def set(self):
        return self.__opts.project is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def organisation(self):
        return None if self.__opts.project is None else self.__opts.project[0]


    @property
    def group(self):
        return None if self.__opts.project is None else self.__opts.project[1]


    @property
    def location(self):
        return None if self.__opts.project is None else self.__opts.project[2]


    @property
    def force(self):
        return self.__opts.force


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
        return "CmdAWSProject:{organisation:%s, group:%s, location:%s, force:%s, delete:%s, verbose:%s}" % \
               (self.organisation, self.group, self.location, self.force, self.delete, self.verbose)
