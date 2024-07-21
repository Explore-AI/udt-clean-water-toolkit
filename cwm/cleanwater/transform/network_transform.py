from ..relations import PipeAndAssets


class NetworkTransform(PipeAndAssets):

    def initialise(
        self, pipe_asset, point_assets: dict, method: str | None = "geodjango"
    ):
        # if method in ["geodjango", "geoalchemy"] and not pipe_model:
        #     raise Exception(
        #         "If the 'geodjango' or 'geoalchemy' method is chosen a 'pipe_model' mush be specified"
        #     )
        self.get_pipe_point_relation_queryset(pipe_asset, point_assets, filters)

        # Logger, Hydrant

        #         subquery4 = self.generate_dwithin_subquery(
        #     pipe_model,
        #     Hydrant.objects.all(),
        #     json_fields,
        #     extra_json_fields={"acoustic_logger": "acoustic_logger"},
        # )

        # subquery5 = self.generate_dwithin_subquery(
        #     pipe_model,
        #     PressureFitting.objects.all(),
        #     json_fields,
        #     extra_json_fields={"subtype": "subtype"},
        # )

        # subquery6 = self.generate_dwithin_subquery(
        #     PressureControlValve.objects.all(),
        #     json_fields,
        #     extra_json_fields={"subtype": "subtype"},
        # )

        # subquery7 = self.generate_dwithin_subquery(
        #     NetworkMeter.objects.all(),
        #     json_fields,
        #     extra_json_fields={"subtype": "subtype"},
        # )

        # subquery8 = self.generate_dwithin_subquery(Chamber.objects.all(), json_fields)

        # subquery9 = self.generate_dwithin_subquery(
        #     OperationalSite.objects.all(),
        #     json_fields,
        #     extra_json_fields={"subtype": "subtype"},
        # )

        # subquery10 = self.generate_dwithin_subquery(
        #     NetworkOptValve.objects.all(),
        #     json_fields,
        #     extra_json_fields={"acoustic_logger": "acoustic_logger"},
        # )

        # subquery11 = self.generate_dwithin_subquery(
        #     ConnectionMeter.objects.all(),
        #     json_fields,
        # )

        # subquery12 = self.generate_dwithin_subquery(
        #     ConsumptionMeter.objects.all(),
        #     json_fields,
        # )

        # subquery13 = self.generate_dwithin_subquery(
        #     ListeningPost.objects.all(),
        #     json_fields,
        # )

        # subquery14 = self.generate_dwithin_subquery(
        #     IsolationValve.objects.all(),
        #     json_fields,
        # )

        # subquery15 = self.generate_dwithin_subquery(
        #     BulkMeter.objects.all(),
        #     json_fields,
        # )

        #         subqueries = {
        #     "logger_data": ArraySubquery(subquery3),
        #     "hydrant_data": ArraySubquery(subquery4),
        #     "pressure_fitting_data": ArraySubquery(subquery5),
        #     "pressure_valve_data": ArraySubquery(subquery6),
        #     "network_meter_data": ArraySubquery(subquery7),
        #     "chamber_data": ArraySubquery(subquery8),
        #     "operational_site_data": ArraySubquery(subquery9),
        #     "network_opt_valve_data": ArraySubquery(subquery10),
        #     "connection_meter_data": ArraySubquery(subquery11),
        #     "consumption_meter_data": ArraySubquery(subquery12),
        #     "listening_post_data": ArraySubquery(subquery13),
        #     "isolation_valve_data": ArraySubquery(subquery14),
        #     "bulk_meter_data": ArraySubquery(subquery15),
        # }
