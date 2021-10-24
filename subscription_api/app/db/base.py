# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base, TimeStampBase  # noqa
from app.models.product import Product  # noqa
from app.models.subscription import Subscription  # noqa
