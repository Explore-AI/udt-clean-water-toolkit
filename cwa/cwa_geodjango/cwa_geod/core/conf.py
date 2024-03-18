import configparser
from itertools import chain
from django.core.exceptions import ValidationError
from .validators import ConfigValidator


class AppConf:
    def __init__(self, conf_file: str):
        """Set the config params from the conf file

        https://stackoverflow.com/a/26859985
        """

        parser = configparser.ConfigParser()

        with open(conf_file) as lines:
            lines = chain(("[app_config]",), lines)  # This line does the trick.
            parser.read_file(lines)

        self._validate_config(parser["app_config"])

    def _validate_config(self, parser_config):
        self.validated_config = ConfigValidator(parser_config)
        if not self.validated_config.is_valid():
            raise ValidationError(
                [
                    ValidationError(_("Error 1"), code="error1"),
                    ValidationError(_("Error 2"), code="error2"),
                ]
            )

    @property
    def method(self):
        return self.config["method"]
