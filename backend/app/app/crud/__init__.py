# from .crud_item import item
from .crud_document import document
from .crud_user import user
from .crud_stripecustomer import stripecustomer
from .crud_lifetime_track import lifetime_track
from .crud_monthly_track import monthly_track
from .crud_lifetime_code import lifetime_code

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
