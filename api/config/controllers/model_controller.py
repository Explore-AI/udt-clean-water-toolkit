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

    def execute_query(self, db_session):
        return db_session.query(self.Model).all()

    def set_get_args(self):
        return {"response_model": list[self.serializer_class]}

    @classmethod
    def list(
        cls,
        request: Request,
        model: UserSerializer = Depends(),
        db_session: Session = Depends(get_db_session),
    ):
        self = request["endpoint"].__self__()
        queryset = self.execute_query(db_session)
        print(queryset)
        return queryset

        # return
        # queryset = self.filter_queryset(self.query)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
