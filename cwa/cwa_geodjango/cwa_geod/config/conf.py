import configparser
from itertools import chain


class AppConf:
    def __init__(self, conf_file: str):
        """Set the config params from the conf file

        https://stackoverflow.com/a/26859985
        """

        parser = configparser.ConfigParser()

        with open(conf_file) as lines:
            lines = chain(("[top]",), lines)  # This line does the trick.
            parser.read_file(lines)

        self.config = parser["top"]

    @property
    def method(self):
        return self.config["method"]
