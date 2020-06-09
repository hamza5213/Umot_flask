from .. import db


def add_to_session(entity):
    try:
        db.session.add(entity)
        return entity
    except Exception as e:
        rollback_changes()
        raise e
    return None


def add_to_db(entity):
    try:
        db.session.add(entity)
        commit_changes()
        return entity
    except Exception as e:
        rollback_changes()
        raise e
    return None


def save_snapshot():
    try:
        commit_changes()
    except Exception as e:
        rollback_changes()
        raise e


def commit_changes():
    db.session.commit()


def rollback_changes():
    db.session.rollback()


def close_session():
    db.session.remove()
