import configparser
from itertools import chain
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
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
        config = ConfigValidator(parser_config)
        is_valid = config.is_valid()

        if not is_valid:
            raise ValidationError(
                [
                    ValidationError(
                        _("Invalid or missing: '%(value)s' - %(error)s"),
                        params={"value": value, "error": error[0]},
                    )
                    for value, error in self.validated_config.errors.items()
                ]
            )

        self.validated_config = config.cleaned_data

    @property
    def method(self):
        return self.validated_config["method"]

    @property
    def srid(self):
        return self.validated_config["srid"]

    @property
    def parallel(self):
        return self.validated_config["parallel"]

    @property
    def query_step(self):
        return self.validated_config["query_step"]

    @property
    def query_limit(self):
        return self.validated_config["query_limit"]

    @property
    def query_offset(self):
        return self.validated_config["query_offset"]
