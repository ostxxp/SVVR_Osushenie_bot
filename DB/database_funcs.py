from DB.database import session as db
from DB.base_models import Prorab, Report

# PRORABS
async def prorab_exists(id):
    return db.query(Prorab).filter_by(id=id).first() is not None


async def add_prorab(id):
    new_prorab = Prorab(id=id, is_filled=0)
    db.add(new_prorab)
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

# REPORTS
async def report_exists(id, date):
    return db.query(Report).filter_by(prorab_id=id, date=date).first() is not None

async def add_report(id, date):
    new_report = Report(prorab_id=id, date=date)
    db.add(new_report)
    db.commit()
    db.close()

async def get_report_date(id):
    return db.query(Report).filter_by(prorab_id=id).first().date
