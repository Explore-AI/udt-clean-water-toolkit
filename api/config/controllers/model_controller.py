# from typing import Optional
from json.decoder import JSONDecodeError
from fastapi import Request, Depends, status, HTTPException
from pydantic import ValidationError as PyValidationError
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config.db import get_db_session
from config.exceptions import (
    MethodNotAllowed,
    ParseError,
    ValidationError,
    SQLAlchemyIntegrityError,
)
from config.settings import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from . import BaseController

# def execute_query(self):
#     session = next(db_session())
#     if self.Model and not self.query != None:
#         return session.query(self.Model).all()
#     # TO DO: have another look at this issue
#     # There appears to be a FastAPI bug with the usage of next(). See link:
#     # https://github.com/tiangolo/fastapi/discussions/7334
#     return session.execute(self.query)


class ModelController(BaseController):
    """This is an abstract base class. It should not be instantiated
    directly. It should only be used as an inherited class.

    https://stackoverflow.com/questions/75249150/how-to-use-class-based-views-in-fastapi
    """

    Model = None
    serializer_class = None
    db_query = None
    allowed_methods = ["get", "put", "put", "delete"]

    def __init__(self):
        """Define all instance attributes here."""
        self.db_session = None
        self.query_params = None
        self.page_size = None
        self.page_num = None
        self.order = None
        self.request = None

    def initial(self, request, db_session):
        """The first method called by this
        controller in the response cycle. We don't
        want to initialise all these attributes
        on class initialisation so we do it here"""

        self.request = request

        if self.get_request_method() not in list(
            map(lambda x: x.lower(), self.allowed_methods)
        ):
            raise MethodNotAllowed()

        self.db_session = db_session
        self.query_params = dict(request._query_params)

        qs = None
        if self.get_db_query() is None:
            qs = select(self.Model)

        return qs

    def get_request_method(self):
        # Certain functions such as the `get_serializer_class`
        # method is called when the router function is instantiated
        # upon compilation. However, the request object is only
        # populated at run time. Therefore, have to check is request
        # object is present first.

        try:
            method = self.request.method.lower()
        except:
            method = None

        return method

    def execute_query(self, qs):
        if self.get_db_query() is not None:
            qs = self.get_db_query()
        return self.db_session.scalars(qs)

    def get_db_query(self):
        """
        To write a custom query overide this method or
        supply the `db_query` class attribute.
        """
        # TO DO: below assert does not make sense
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

    def set_generic_args(self, args={}):
        generic_args = {}
        return args | generic_args

    def set_get_args(self):
        args = {"response_model": list[self.get_serializer_class()]}
        return self.set_generic_args(args)

    def set_post_args(self):
        args = {"response_model": self.get_serializer_class(), "status_code": 201}
        return self.set_generic_args(args)

    def set_delete_args(self):
        return self.set_generic_args()

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

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(**self.query_params)

        validated_query_params = {
            k: v for k, v in serializer.model_dump().items() if v is not None
        }

        return validated_query_params

    def order_queryset(self, queryset):
        """Construct order query param as follows:
        `order=field__asc` or `order=field_dsc`"""

        field = self.order.split("__")[0]
        ordering = self.order.split("__")[1]

        attr = getattr(self.Model, field)
        if ordering == "asc":
            queryset = queryset.order_by(attr)
        elif ordering == "dsc":
            queryset = queryset.order_by(attr.desc())
        return queryset

    def filter_queryset(self, queryset, validated_query_params):
        """Filter validated query params using the
        AND operator.

        TO DO: Filter by OR
        TO DO: Filter across joins
        """

        for k, v in validated_query_params.items():
            attr = getattr(self.Model, k)
            queryset = queryset.where(attr == v)

        if self.order:
            queryset = self.order_queryset(queryset)

        return queryset

    def paginate_queryset(self, queryset):
        page_limit = self.page_size or DEFAULT_PAGE_SIZE

        if page_limit > MAX_PAGE_SIZE:
            page_limit = MAX_PAGE_SIZE

        # TO DO: Have to use limit while working with sqlite.
        # Proper implmentation is with fetch but sqlite not yet supported
        # https://stackoverflow.com/a/77379809
        return queryset.limit(page_limit)

    def serialize_data(self, serializer_class, data):
        """Serialize the body of a request"""
        try:
            return serializer_class(**data)
        except PyValidationError as e:
            raise ValidationError(detail=e.json())

    def _get_object_or_404(self, pk):

        obj = self.db_session.get(self.Model, pk)
        print(obj, "hhhhhh")
        if obj:
            return obj

        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Object not found")

    async def get_object(self):
        """
        Returns the object the controller is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups. Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        data = await self.get_json_data()

        serializer_class = self.get_serializer_class()
        serializer = self.serialize_data(serializer_class, data)

        obj = self._get_object_or_404(serializer.id)

        # TO DO: May raise a permission denied
        #self.check_object_permissions(self.request, obj)

        return obj

    def create_obj(self, serializer):
        validated_data = serializer.model_dump()

        new_obj = self.Model(**validated_data)

        self.db_session.add(new_obj)

        try:
            self.db_session.commit()
        except IntegrityError:
            raise SQLAlchemyIntegrityError()

        self.db_session.refresh(new_obj)

        return new_obj

    def destroy_obj(self, obj):
        self.db_session.delete(obj)
        self.db_session.commit()

    async def get_json_data(self):

        try:
            data = await self.request.json()
        except JSONDecodeError:
            raise ParseError(detail="Did not receive valid JSON")
        except ValueError:
            raise ParseError(detail="Did not receive valid JSON")

        return data

    @classmethod
    def list(
        cls,
        request: Request,
        db_session: Session = Depends(get_db_session),
    ):
        """This method is bound to GET requests on this
        controller. It is the endpoint function for the
        FastAPI @get method.
        """

        self = request["endpoint"].__self__()
        queryset = self.initial(request, db_session)

        validated_query_params = self.validate_query_params()

        if self.get_db_query() is None:
            queryset = self.filter_queryset(queryset, validated_query_params)
            queryset = self.paginate_queryset(queryset)

        queryset = self.execute_query(queryset)

        return queryset

    @classmethod
    async def create(
        cls,
        request: Request,
        db_session: Session = Depends(get_db_session),
    ):
        """This method is bound to POST requests on this
        controller. It is the endpoint function for the
        FastAPI @post method.
        """
        self = request["endpoint"].__self__()
        self.initial(request, db_session)

        data = await self.get_json_data()

        serializer_class = self.get_serializer_class()
        serializer = self.serialize_data(serializer_class, data)

        new_obj = self.create_obj(serializer)

        return new_obj

    @classmethod
    async def destroy(cls,
        request: Request,
        db_session: Session = Depends(get_db_session),
    ):
        """This method is bound to DELETE requests on this
        controller. It is the endpoint function for the
        FastAPI @delete method.
        """
        self = request["endpoint"].__self__()
        self.initial(request, db_session)
        obj = await self.get_object()
        self.destroy_obj(obj)
        return {"message": "success"}
