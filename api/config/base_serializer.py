from typing import Optional
from pydantic import BaseModel, create_model


# https://stackoverflow.com/a/67733889
# ModelMetaClass is now private with pydantic v2 https://github.com/pydantic/pydantic/issues/6381
# class AllOptional(ModelMetaClass):
#     """Create metaclass that allows all fields on a pydantic
#     model to be set as optional. This has been requested as a pydantic
#     feature but it appeards the decision has been made to not implement it.
#     https://github.com/pydantic/pydantic/issues/3120

#     Use it by passing the metaclass arg into your inhereited model:
#     metaclass=AllOptional
#     """

#     def __new__(
#         self, name: str, bases: Tuple[type], namespaces: Dict[str, Any], **kwargs
#     ):
#         annotations: dict = namespaces.get("__annotations__", {})

#         for base in bases:
#             for base_ in base.__mro__:
#                 if base_ is BaseModel:
#                     break

#                 annotations.update(base_.__annotations__)

#         for field in annotations:
#             if not field.startswith("__"):
#                 annotations[field] = Optional[annotations[field]]

#         namespaces["__annotations__"] = annotations

#         return super().__new__(mcs, name, bases, namespaces, **kwargs)


class BaseSerializer(BaseModel):
    class Config:
        from_attributes = True
        validate_assignment = True
