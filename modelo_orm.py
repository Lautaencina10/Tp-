from peewee import *

sqlite_db = SqliteDatabase("obras_urbanas.db")


class BaseModel(Model):
    class Meta:
        database = sqlite_db


class Obra(BaseModel):
    nombre = CharField(null=True)
    direccion = CharField(null=True)
    monto_contrato = FloatField(null=True)
    porcentaje_avance = FloatField(null=True)
