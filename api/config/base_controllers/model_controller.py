from typing import Optional
from config.db import db_session
from config.routers import ModelRouter
from fastapi import Depends
from core.serializers.user_serializer import UserSerializer


class ModelController(ModelRouter):
    Model = None
    query = None
    serializer_class = None
    # TO DO: apparantly the getter for __fields__ is deprecated

    def _get_args(self):
        return dict([(i, None) for i in list(self.serializer_class.__fields__.keys())])

    def get_attr(self):
        return ModelController.__dict__.items()

    def execute_query(self):
        session = next(db_session())
        if self.Model and not self.query != None:
            return session.query(self.Model).all()
        # TO DO: have another look at this issue
        # There appears to be a FastAPI bug with the usage of next(). See link:
        # https://github.com/tiangolo/fastapi/discussions/7334
        return session.execute(self.query)

    def initialise_request(self, *args, **kwargs):
        # self.list()
        return
        # self._get(*args, response_model=self.serializer_class, **kwargs)

    # https://stackoverflow.com/questions/75249150/how-to-use-class-based-views-in-fastapi
    def list_data(name: str = None, id: Optional[int] = None):
        # model: UserSerializer = Depends()

        return [{"name": "yellow"}]
        # return
        # queryset = self.filter_queryset(self.query)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)

    # @app.get("/users/", response_model=list[serializer_class])
    # def get(self):
    #     self.execute_query()

    # def get_users(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.User).offset(skip).limit(limit).all()

    # def create_user(db: Session, user: schemas.UserCreate):
    #     fake_hashed_password = user.password + "notreallyhashed"
    #     db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    #     db.add(db_user)
    #     db.commit()
    #     db.refresh(db_user)
    #     return db_user

    # def get_items(db: Session, skip: int = 0, limit: int = 100):
    #     return db.query(models.Item).offset(skip).limit(limit).all()

    # def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    #     db_item = models.Item(**item.dict(), owner_id=user_id)
    #     db.add(db_item)
    #     db.commit()
    #     db.refresh(db_item)
    #     return db_item
