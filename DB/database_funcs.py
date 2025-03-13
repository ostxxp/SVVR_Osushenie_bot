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

async def filled(id, flag):
    prorab = db.query(Prorab).filter_by(id=id).first()
    if prorab:
        if flag:
            prorab.is_filled = 1
        else:
            prorab.is_filled = 0
        db.commit()
        db.close()

async def get_prorabs():
    return db.query(Prorab).all()

# REPORTS
async def report_exists(id, date):
    return db.query(Report).filter_by(prorab_id=id, date=date).first() is not None

async def add_report(id, object_name, prorab_name):
    new_report = Report(prorab_id=id, object_name=object_name, prorab_name=prorab_name)
    db.add(new_report)
    db.commit()
    db.close()

async def add_date(id, date):
    report = db.query(Report).filter_by(prorab_id=id).first()
    if report:
        report.date = date
        db.commit()
        db.close()

async def get_report_date(id):
    return db.query(Report).filter_by(prorab_id=id).first().date

async def get_installers(id):
    return db.query(Report).filter_by(prorab_id=id).first().installers

async def add_installer(id, installer):
    report = db.query(Report).filter_by(prorab_id=id).first()
    if report:
        text = ""
        if db.query(Report).filter_by(prorab_id=id).first().installers is not None:
            text = db.query(Report).filter_by(prorab_id=id).first().installers
        report.installers = text + installer + ","
        db.commit()
        db.close()

async def remove_installer(id, installer):
    report = db.query(Report).filter_by(prorab_id=id).first()
    if report:
        installers = db.query(Report).filter_by(prorab_id=id).first().installers
        installers = installers.replace(f"{installer} ", "")
        report.installers = installers
        db.commit()
        db.close()

async def clear_reports(id):
    report = db.query(Report).filter_by(prorab_id=id).first()
    if report:
        db.delete(report)
        db.commit()
        db.close()


async def get_obj_name(id):
    return db.query(Report).filter_by(prorab_id=id).first().object_name

async def set_column(id, column):
    report = db.query(Report).filter_by(prorab_id=id).first()
    if report:
        report.column = column
        db.commit()
        db.close()

async def get_column(id):
    return db.query(Report).filter_by(prorab_id=id).first().column