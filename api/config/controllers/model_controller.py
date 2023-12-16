# from typing import Optional
from fastapi import Request, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from config.db import get_db_session
from config.settings import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE

# def execute_query(self):
#     session = next(db_session())
#     if self.Model and not self.query != None:
#         return session.query(self.Model).all()
#     # TO DO: have another look at this issue
#     # There appears to be a FastAPI bug with the usage of next(). See link:
#     # https://github.com/tiangolo/fastapi/discussions/7334
#     return session.execute(self.query)


class ModelController:
    """This is an abstract base class. It should not be
    instantiated directly. It should only be used as an inherited
    class.

    # https://stackoverflow.com/questions/75249150/how-to-use-class-based-views-in-fastapi
    """

    Model = None
    serializer_class = None
    db_query = None

    def __init__(self):
        """Define all instance attributes here."""
        self.db_session = None
        self.query_params = None
        self.validated_query_params = None
        self.session_query = None
        self.page_size = None
        self.page_num = None
        self.order = None

    def initial(self, request, db_session):
        """The first method called by this
        controller in the response cycle. We don't
        want to initialise all these attributes
        on class initialisation so we do it here"""

        self.db_session = db_session
        self.query_params = dict(request._query_params)

        if not self.db_query:
            self.session_query = select(self.Model)

    def execute_query(self):
        if not self.get_db_query():
            print(self.session_query)
            return self.db_session.scalars(self.session_query)
        return self.get_db_query()

    def get_db_query(self):
        assert self.db_query is not None or self.Model is not None, (
            f"'{self.__class__.__name__}' should either include a Model attribute"
            ", a `db_query` attribute, or override the `get_db_query()` method."
        )
        return self.db_query

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
            f"'{self.__class__.__name__}' should either include a `serializer_class` attribute, "
            "or override the `get_serializer_class()` method."
        )
        return self.serializer_class

    def set_get_args(self):
        return {"response_model": list[self.get_serializer_class()]}

    def validate_query_params(self):
        page_size = self.query_params.pop("page_size", None)
        page_num = self.query_params.pop("page_num", None)
        self.order = self.query_params.pop("order", None)

        try:
            if page_size:
                self.page_size = int(page_size)
        except ValueError:
            raise ValueError("Got non-integer argument for 'page_size' query paramter")

        try:
            if page_num:
                self.page_num = int(page_num)
        except ValueError:
            raise ValueError("Got non-integer argument for 'page_num' query paramter")

        serializer = self.get_serializer_class()
        validated_serializer = serializer(**self.query_params)
        self.validated_query_params = {
            k: v for k, v in dict(validated_serializer).items() if v is not None
        }

    # def order_queryset(self):
    #     if self.order == "asc":
    #         self.session_query.order_by(''

    def filter_queryset(self):
        """Filter validated query params using the
        AND operator.

        TO DO: Filter by OR
        TO DO: Filter across joins
        """

        q = self.session_query
        for k, v in self.validated_query_params.items():
            f = getattr(self.Model, k)
            q = q.where(f == v)

        self.session_query = q

    #        self.order_queryset()

    def paginate_queryset(self):
        page_limit = self.page_size or DEFAULT_PAGE_SIZE

        if page_limit > MAX_PAGE_SIZE:
            page_limit = MAX_PAGE_SIZE

        # TO DO: Have to use limit while working with sqlite.
        # Proper implmentation is with fetch but sqlite not yet supported
        # https://stackoverflow.com/a/77379809
        self.session_query = self.session_query.limit(page_limit)

    @classmethod
    def list(
        cls,
        request: Request,
        db_session: Session = Depends(get_db_session),
    ):
        """This method is bound to GET requests on this
        controller. It is the endpoint function for the
        FastAPI get method.

        """

        self = request["endpoint"].__self__()
        self.initial(request, db_session)

        self.validate_query_params()

        if not self.db_query:
            self.filter_queryset()
            self.paginate_queryset()

        queryset = self.execute_query()
        return queryset
