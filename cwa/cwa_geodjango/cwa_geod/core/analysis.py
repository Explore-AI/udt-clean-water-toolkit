from cwa_geod.config.conf import AppConf


class Analysis(AppConf):
    args = self._set_args()
    super().__init__(args.file)

    def _set_args(self):
        parser = argparse.ArgumentParser(
            description="Run Clean Water Toolkit functions"
        )

        parser.add_argument(
            "--method",
            help="Convert the gis network to a connected graph network.",
            action="append",
        )

        parser.add_argument("-f", "--file")

        return parser.parse_args()
