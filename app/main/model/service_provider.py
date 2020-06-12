from . import Identity
from .. import db


class ServiceProvider(Identity):
    __tabelname__ = "service_providers"
    tmdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    quality = db.Column(db.String, nullable=False)
    locale = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey("providers.id"), nullable=False)
    providers = db.relationship("Providers", back_populates="service_provider")
