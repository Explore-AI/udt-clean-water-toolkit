# from typing import Optional
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from config.db import get_db_session
from config.settings import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


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
        self.query_params = dict(request._query_params)
        self.query = self.db_session.query(self.Model)

    def construct_query(self, **kwargs):
        q = self.query
        for k, v in kwargs.items():
            f = getattr(self.Model, k)
            q = q.filter(f.in_(v))
        self.query = q

    def execute_query(self):
        return self.query.all()

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            "'%s' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method." % self.__class__.__name__
        )
        return self.serializer_class

    def set_get_args(self):
        return {"response_model": list[self.get_serializer_class()]}

    def validate_query_params(self):
        page_size = self.query_params.pop("page_size", None)
        page_num = self.query_params.pop("page_num", None)
        order = self.query_params.pop("order", None)

        try:
            page_size = int(page_size)
        except:
            raise TypeError("Got non-integer argument for 'page_size' query paramter")

        self.validated_query_params = self.get_serializer_class(**self.query_params)
        return page_size

    def filter_queryset(self):
        pass

    def paginate_queryset(self, page_size):
        page_limit = page_size or DEFAULT_PAGE_SIZE

        # if page_limit > MAX_PAGE_SIZE:
        #     page_limit = MAX_PAGE_SIZE

        self.query = self.query.limit(page_limit)

    @classmethod
    def list(
        cls,
        request: Request,
        db_session: Session = Depends(get_db_session),
    ):
        self = request["endpoint"].__self__()
        self.initial(request, db_session)
        page_size = self.validate_query_params()
        self.filter_queryset()

        self.paginate_queryset(page_size)

        queryset = self.query.all()

        return queryset

        # return
        # queryset = self.filter_queryset(self.query)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
