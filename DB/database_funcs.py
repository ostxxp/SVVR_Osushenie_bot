from DB.database import session as db
from DB.base_models import Prorab, Report
from DB import objects_fetching

# PRORABS
async def prorab_exists(id):
    return db.query(Prorab).filter_by(id=id).first() is not None

async def object_filled(id, obj_name):
    prorab = db.query(Prorab).filter_by(id=id).first()
    if prorab:
        objects = prorab.objects_left
        if objects is None:
            await filled(id, True)
        else:
            prorab.objects_left = objects.replace(f"{obj_name}|", "")
            if prorab.objects_left.count('|') == 0:
                await filled(id, True)
        db.commit()
        db.close()

async def set_objects(id, objects):
    prorab = db.query(Prorab).filter_by(id=id).first()
    if prorab:
        prorab.objects_left = objects
        db.commit()
        db.close()

async def get_unfilled_objects(id):
    objs = await objects_fetching.fetch_objects_names(id)
    unfilled_objs = db.query(Prorab).filter_by(id=id).first().objects_left
    for obj in unfilled_objs[:-1].split('|'):
        if obj not in objs:
            unfilled_objs = unfilled_objs.replace(f"{obj}|", "")
            db.commit()
    return db.query(Prorab).filter_by(id=id).first().objects_left[:-1].split('|')


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

async def remove_prorab(id):
    prorab = db.query(Prorab).filter_by(id=id).first()
    if prorab:
        db.delete(prorab)
        db.commit()

    # REPORTS
async def report_exists(id, date):
    return db.query(Report).filter_by(prorab_id=id, date=date).first() is not None

async def add_report(id, object_name, prorab_name):
    report = db.query(Report).filter_by(prorab_id=id).first()
    if report:
        db.delete(report)
        db.commit()
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
        installers = installers.replace(f"{installer},", "")
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