from DB.database import session as db
from DB.base_models import Prorab, Installer

async def prorab_exists(id):
    return db.query(Prorab).filter_by(id=id).first() is not None

async def installer_exists(id):
    return db.query(Installer).filter_by(id=id).first() is not None

async def add_prorab(id):
    new_user = Prorab(id=id, is_filled=0)
    db.add(new_user)
    db.commit()
    db.close()

async def add_installer(id):
    new_user = Installer(id=id)
    db.add(new_user)
    db.commit()
    db.close()

async def is_filled(id):
    if db.query(Prorab).filter_by(id=id).first().is_filled:
        db.close()
        return True
    db.close()
    return False

async def get_prorabs():
    return db.query(Prorab).all()
