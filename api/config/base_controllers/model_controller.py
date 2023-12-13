from config.db import db_session


class ModelController:
    Model = None
    query = None

    # There appears to be a FastAPI bug with the usage of next(). See link:
    # https://github.com/tiangolo/fastapi/discussions/7334

    def get_queryset(self):
        session = next(db_session())
        if self.Model and not self.query != None:
            return session.query(self.Model).all()
        print(self.query)
        import pdb

        pdb.set_trace()
        return session.execute(self.query)
        # return db.query(self.queryset)
        # return db.query(models.User).filter(models.User.id == user_id).first()

    # def get_user_by_email(db: Session, email: str):
    #     return db.query(models.User).filter(models.User.email == email).first()

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
