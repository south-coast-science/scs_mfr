"""
Created on 8 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse

from scs_mfr import version


# --------------------------------------------------------------------------------------------------------------------

class CmdAirNowSiteConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog { -c | -p | [-s COUNTRY LOC IS_MOBILE] "
                                                    "[-o PARAM POC] [-d PARAM] } [-v]", version=version())

        # fields...
        self.__parser.add_option("--countries", "-c", action="store_true", dest="countries", default=False,
                                 help="list the available countries to stdout")

        self.__parser.add_option("--parameters", "-p", action="store_true", dest="parameters", default=False,
                                 help="list the available parameters to stdout")

        self.__parser.add_option("--site", "-s", type="int", nargs=3, action="store", dest="site",
                                 help="set site country code, 9 digit location code and mobile status (1 or 0)")

        self.__parser.add_option("--poc", "-o", type="int", nargs=2, action="store", dest="poc",
                                 help="add or update a parameter occurrence code")

        # delete...
        self.__parser.add_option("--delete", "-d", type="int", action="store", dest="delete",
                                 help="delete a parameter occurrence code")

        # output...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.countries and self.parameters:
            return False

        if (self.countries or self.parameters) and (self.is_set_site() or self.is_set_poc() or self.is_delete_poc()):
            return False

        if self.is_set_site() and self.__opts.site[2] != 0 and self.__opts.site[2] != 1:
            return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def is_set_site(self):
        return self.__opts.site is not None


    def is_set_poc(self):
        return self.__opts.poc is not None


    def is_delete_poc(self):
        return self.__opts.delete is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def countries(self):
        return self.__opts.countries


    @property
    def parameters(self):
        return self.__opts.parameters


    @property
    def site_country_code(self):
        return None if self.__opts.site is None else self.__opts.site[0]


    @property
    def site_location_code(self):
        return None if self.__opts.site is None else self.__opts.site[1]


    @property
    def site_is_mobile(self):
        return None if self.__opts.site is None else (self.__opts.site[2] == 1)


    @property
    def poc_parameter_code(self):
        return None if self.__opts.poc is None else self.__opts.poc[0]


    @property
    def poc_code(self):
        return None if self.__opts.poc is None else self.__opts.poc[1]


    @property
    def poc_delete(self):
        return self.__opts.delete


    @property
    def verbose(self):
        return self.__opts.verbose


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdAirNowSiteConf:{countries:%s, parameters:%s, site:%s, poc:%s, delete:%s, verbose:%s}" %  \
               (self.countries, self.parameters, self.__opts.site, self.__opts.poc, self.poc_delete, self.verbose)
