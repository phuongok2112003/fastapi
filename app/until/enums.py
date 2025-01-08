from enum import Enum
from sqlalchemy.orm import class_mapper
from sqlalchemy import inspect
from typing import Type

class OrderBy(Enum):
   DESC= "desc"
   ASC= "asc"
class FriendshipStatus(Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
def generate_enum_from_model(model: Type) -> Type[Enum]:
    
    # Get the columns of the model
    columns = [column.name for column in inspect(model).c]

    # Create the Enum dynamically
    enum_dict = {col: col for col in columns}
    
    # Create and return Enum class
    return Enum(model.__name__ + "Fields", enum_dict)



