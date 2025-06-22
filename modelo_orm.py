from peewee import *

sqlite_db = SqliteDatabase('obras_urbanas.db', pragmas={'journal_mode': 'wal'})

class BaseModel(Model):
    class Meta:
        database = sqlite_db

class Comuna(BaseModel):
    Id_Comuna = AutoField()
    Comuna = CharField()

class Barrio(BaseModel):
    Id_barrio = AutoField()
    Barrio = CharField()
    Comuna = ForeignKeyField(Comuna, backref='barrios')

class Obra(BaseModel):
    Id_Obra = AutoField()
    Nombre_obra = TextField()
    Etapa = TextField()
    Descripcion = TextField(null=True)
    Direccion = TextField(null=True)
    Monto_contrato = FloatField(null=True)
    Porcentaje_avance = FloatField(null=True)
    Plazo = IntegerField(null=True)
    Barrio = ForeignKeyField(Barrio, backref='obras', null=True)
