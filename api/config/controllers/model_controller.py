from typing import Optional
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from config.db import get_db_session
from core.serializers.user_serializer import UserSerializer


class ModelController:
    # https://stackoverflow.com/questions/75249150/how-to-use-class-based-views-in-fastapi
    Model = None
    query = None
    serializer_class = None

    # def execute_query(self):
    #     session = next(db_session())
    #     if self.Model and not self.query != None:
    #         return session.query(self.Model).all()
    #     # TO DO: have another look at this issue
    #     # There appears to be a FastAPI bug with the usage of next(). See link:
    #     # https://github.com/tiangolo/fastapi/discussions/7334
    #     return session.execute(self.query)

    def initial(self, request, db_session):
        self.db_session = db_session
        self.query_params = request._query_params

    def construct_query(self, **kwargs):
        q = self.db_session.query(self.Model)
        for k, v in kwargs.items():
            f = getattr(self.Model, k)
            q = q.filter(f.in_(v))
        return q

    def execute_query(self):
        return self.db_session.query(self.Model).all()

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )
        return self.serializer_class

    def set_get_args(self):
        return {"response_model": list[self.get_serializer_class()]}

    def get_validated_params(self):
        validated_params = self.get_serializer_class(**self.query_params)
        return validated_params

    def filter_queryset(self):
        pass

    def paginate_queryset(self):
        x = {"page_limit": 100}
        query = self.construct_query(**x)
        return query

    @classmethod
    def list(
        cls,
        request: Request,
        db_session: Session = Depends(get_db_session),
    ):
        self = request["endpoint"].__self__()
        self.initial(request)

        self.filter_queryset()

        self.paginate_queryset()

        queryset = self.execute_query()

        return queryset

        # return
        # queryset = self.filter_queryset(self.query)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
