from . import Identity
from .. import db


class Providers(Identity):
    __tabelname__ = "providers"
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    service_provider = db.relationship("ServiceProvider")
