from DB.database import session as db
from DB.base_models import Admin

def is_admin(id):
    return db.query(Admin).filter_by(id=id).first()